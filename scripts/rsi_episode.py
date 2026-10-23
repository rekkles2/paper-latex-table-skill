"""Track immutable table-learning episodes: paired, image-only, or design reuse.

Records evidence and reviewer attestations, not automatic vision or promotion.
Operational state stays outside the stable skill; no stable files are modified.
"""
import argparse
import hashlib
import json
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from learning import default_state
from tablelib import ROOT, read_json, sha256, write_json

CHECKS = ('data', 'compilation', 'visual', 'typography', 'readability', 'constraints')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def snapshot(paths, folder):
    paths = [Path(p).resolve() for p in paths]
    if any(not p.is_file() for p in paths): raise ValueError('Every artifact must be an existing file')
    folder.mkdir(parents=True, exist_ok=False)
    records = []
    for i, path in enumerate(paths):
        target = folder / (str(i) + '-' + path.name)
        before = sha256(path); shutil.copyfile(path, target)
        if sha256(target) != before: raise ValueError('Input changed during snapshot')
        records.append({'path': target.name, 'sha256': before, 'original_path': str(path)})
    return records


def intact(folder, records, expected_hash=None):
    if expected_hash is not None and digest(records) != expected_hash:
        raise ValueError('Artifact manifest digest changed')
    for record in records:
        p = (folder / record['path']).resolve()
        if not p.is_relative_to(folder.resolve()) or sha256(p) != record['sha256']:
            raise ValueError('Stale or tampered artifact')


def start(state, mode, sources, requirements):
    state = state.resolve()
    if state.is_relative_to(ROOT.resolve()): raise ValueError('State must be outside the stable skill')
    if mode not in ('paired', 'image-only', 'reuse'): raise ValueError('Unknown learning mode')
    req = read_json(requirements)
    if not req.get('goal') or not req.get('constraints'): raise ValueError('Declare goal and constraints')
    if mode == 'paired' and not (any(p.suffix.lower() == '.tex' for p in sources) and any(p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.pdf') for p in sources)):
        raise ValueError('Paired mode needs actual code and reference image/PDF')
    if mode == 'image-only' and not any(p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.pdf') for p in sources):
        raise ValueError('Image-only mode needs a reference image/PDF')
    folder = state / 'episodes' / uuid.uuid4().hex
    artifacts = snapshot([*sources, requirements], folder / 'inputs')
    entry = {'schema_version': 1, 'mode': mode, 'requirements': req,
             'sources': artifacts, 'input_hash': digest(artifacts), 'status': 'captured',
             'created_utc': datetime.now(timezone.utc).isoformat(), 'rights': 'unknown-local-only'}
    write_json(folder / 'episode.json', entry)
    return folder


def candidate(episode, tex, artifacts, recipe):
    entry = read_json(episode / 'episode.json'); intact(episode / 'inputs', entry['sources'], entry['input_hash'])
    design = read_json(recipe)
    if not design.get('reason') or not design.get('parents'):
        raise ValueError('Candidate recipe needs parents and a concrete reason')
    # Cap independent designs; iterative repairs use a new episode linked as a parent.
    candidates = episode / 'candidates'
    if candidates.exists() and len(list(candidates.iterdir())) >= 3:
        raise ValueError('At most three candidates per episode; create a linked repair episode')
    if tex.suffix.lower() != '.tex': raise ValueError('Candidate must include editable TeX')
    ident = uuid.uuid4().hex[:12]; folder = candidates / ident
    files = snapshot([tex, recipe, *artifacts], folder / 'artifacts')
    item = {'candidate_id': ident, 'input_hash': entry['input_hash'], 'artifacts': files,
            'candidate_hash': digest(files), 'recipe': design, 'recipe_artifact': files[1]['path'], 'status': 'generated_unreviewed'}
    write_json(folder / 'candidate.json', item)
    return folder


def review(episode, candidate_id, review_file):
    if not re.fullmatch('[a-f0-9]{12}', candidate_id): raise ValueError('Invalid candidate ID')
    entry = read_json(episode / 'episode.json'); intact(episode / 'inputs', entry['sources'], entry['input_hash'])
    folder = episode / 'candidates' / candidate_id
    item = read_json(folder / 'candidate.json'); intact(folder / 'artifacts', item['artifacts'], item['candidate_hash'])
    if (folder / 'review.json').exists(): raise ValueError('Review is immutable; new repairs need a linked episode')
    report = read_json(review_file)
    if report.get('candidate_hash') != item['candidate_hash'] or report.get('input_hash') != entry['input_hash']:
        raise ValueError('Review must bind candidate and original input hashes')
    if not report.get('reviewer') or report.get('review_type') not in ('self_review', 'independent_review'):
        raise ValueError('Declare actual reviewer and exposure')
    checks = list(CHECKS)
    if entry['mode'] == 'image-only': checks.append('transcription')
    if entry['mode'] == 'paired': checks.append('source_conflicts')
    for check in checks:
        value = report.get('checks', {}).get(check, {})
        if value.get('status') not in ('passed', 'failed', 'pending') or not value.get('evidence'):
            raise ValueError('Need explicit status and artifact evidence for ' + check)
        # Paths refer to immutable candidate snapshots, never unstored transient files.
        known = {a['path'] for a in item['artifacts']}
        if any(p not in known for p in value['evidence']): raise ValueError('Evidence must reference snapshotted artifacts')
    if not isinstance(report.get('unresolved_semantic_cells'), int) or report['unresolved_semantic_cells'] < 0:
        raise ValueError('Declare an explicit nonnegative unresolved semantic cell count')
    report['local_reuse_eligible'] = all(report['checks'][c]['status'] == 'passed' for c in checks) and report.get('unresolved_semantic_cells', 0) == 0
    report['status'] = 'reviewed_local' if report['local_reuse_eligible'] else 'needs_revision'
    report['stable_promotion'] = 'not_granted; use controlled RSI proposal'
    write_json(folder / 'review.json', report)
    return report


def select(episode, candidate_id, reason):
    if not re.fullmatch('[a-f0-9]{12}', candidate_id): raise ValueError('Invalid candidate ID')
    if not reason.strip(): raise ValueError('Explain selection against constraints and baseline')
    entry = read_json(episode / 'episode.json'); intact(episode / 'inputs', entry['sources'], entry['input_hash'])
    folder = episode / 'candidates' / candidate_id
    item = read_json(folder / 'candidate.json'); intact(folder / 'artifacts', item['artifacts'], item['candidate_hash'])
    report = read_json(folder / 'review.json')
    if not report.get('local_reuse_eligible'): raise ValueError('Candidate has unresolved checks')
    if report['candidate_hash'] != item['candidate_hash'] or report['input_hash'] != entry['input_hash']:
        raise ValueError('Stale review')
    if entry['mode'] == 'reuse' and not report.get('baseline_comparison'):
        raise ValueError('Design reuse requires an explicit baseline comparison')
    result = {'candidate_id': candidate_id, 'candidate_hash': item['candidate_hash'],
              'review_sha256': sha256(folder / 'review.json'), 'reason': reason,
              'status': 'selected_for_task_and_local_reuse', 'stable_files_changed': False}
    if (episode / 'selection.json').exists(): raise ValueError('Selection is immutable')
    write_json(episode / 'selection.json', result)
    return result


def extract_atom(episode, design_file):
    """Store declarative style parameters only; never reuse past numeric cells."""
    selection, folder, item = checked_selection(episode)
    if read_json(folder / 'artifacts' / item['recipe_artifact']) != item['recipe']:
        raise ValueError('Candidate recipe metadata changed')
    config = read_json(design_file)
    validate_atom_config(config)
    if config != {k: item['recipe'].get(k) for k in config}:
        raise ValueError('Only reviewed candidate design parameters may become an atom')
    entry = {'schema_version': 1, 'version': 1, 'config': config,
             'source_episode': str(episode.resolve()), 'selection_sha256': sha256(episode / 'selection.json'),
             'candidate_hash': item['candidate_hash'], 'review_sha256': selection['review_sha256'],
             'status': 'reviewed_local', 'scope': 'style parameters only; no experimental cells',
             'requires': {'max_header_layers': 1, 'preserve_comparison_groups': True}}
    entry['atom_id'] = digest(entry)[:20]
    output = episode.parent.parent / 'atoms' / (entry['atom_id'] + '.json')
    if output.exists(): raise ValueError('Atom already recorded')
    write_json(output, entry)
    return output


def validate_atom_config(config):
    if set(config) != {'tabcolsep_pt', 'arraystretch', 'group_weight'}:
        raise ValueError('Atoms support spacing and group typography only; arbitrary TeX is not executable configuration')
    if not isinstance(config['tabcolsep_pt'], (int, float)) or not 2 <= config['tabcolsep_pt'] <= 10:
        raise ValueError('Unsupported column spacing')
    if not isinstance(config['arraystretch'], (int, float)) or not .9 <= config['arraystretch'] <= 1.5:
        raise ValueError('Unsupported row spacing')
    if config['group_weight'] not in ('italic', 'bold-italic'):
        raise ValueError('Unsupported group typography')


def load_atom(path):
    atom = read_json(path); validate_atom_config(atom['config'])
    if atom['atom_id'] != digest({k: v for k, v in atom.items() if k != 'atom_id'})[:20]:
        raise ValueError('Design atom content changed')
    episode = Path(atom['source_episode']); selection, folder, item = checked_selection(episode)
    if read_json(folder / 'artifacts' / item['recipe_artifact']) != item['recipe']:
        raise ValueError('Candidate recipe metadata changed')
    if atom['config'] != {k: item['recipe'].get(k) for k in atom['config']}:
        raise ValueError('Atom differs from its reviewed recipe')
    if atom['status'] != 'reviewed_local' or sha256(episode / 'selection.json') != atom['selection_sha256'] or sha256(folder / 'review.json') != atom['review_sha256'] or item['candidate_hash'] != atom['candidate_hash']:
        raise ValueError('Stale design atom evidence')
    return atom


def checked_selection(episode):
    entry = read_json(episode / 'episode.json')
    intact(episode / 'inputs', entry['sources'], entry['input_hash'])
    selection = read_json(episode / 'selection.json')
    if not re.fullmatch('[a-f0-9]{12}', selection['candidate_id']): raise ValueError('Invalid candidate identity')
    folder = episode / 'candidates' / selection['candidate_id']
    item = read_json(folder / 'candidate.json')
    intact(folder / 'artifacts', item['artifacts'], item['candidate_hash'])
    report = read_json(folder / 'review.json')
    if (item['input_hash'] != entry['input_hash'] or report['input_hash'] != entry['input_hash']
            or report['candidate_hash'] != item['candidate_hash'] or selection['candidate_hash'] != item['candidate_hash']
            or sha256(folder / 'review.json') != selection['review_sha256'] or not report.get('local_reuse_eligible')):
        raise ValueError('Selected candidate/input/review chain changed')
    return selection, folder, item


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='action', required=True)
    q = sub.add_parser('start'); q.add_argument('--state', type=Path, default=default_state()); q.add_argument('--mode', choices=['paired', 'image-only', 'reuse'], required=True)
    q.add_argument('--source', type=Path, action='append', required=True); q.add_argument('--requirements', type=Path, required=True)
    q = sub.add_parser('candidate'); q.add_argument('episode', type=Path); q.add_argument('--tex', type=Path, required=True); q.add_argument('--artifact', type=Path, action='append', default=[]); q.add_argument('--recipe', type=Path, required=True)
    q = sub.add_parser('review'); q.add_argument('episode', type=Path); q.add_argument('candidate'); q.add_argument('--review', type=Path, required=True)
    q = sub.add_parser('select'); q.add_argument('episode', type=Path); q.add_argument('candidate'); q.add_argument('--reason', required=True)
    q = sub.add_parser('extract'); q.add_argument('episode', type=Path); q.add_argument('--design', type=Path, required=True)
    q = sub.add_parser('atoms'); q.add_argument('--state', type=Path, default=default_state())
    a = p.parse_args()
    if a.action == 'start': result = str(start(a.state, a.mode, a.source, a.requirements))
    elif a.action == 'candidate': result = str(candidate(a.episode, a.tex, a.artifact, a.recipe))
    elif a.action == 'review': result = review(a.episode, a.candidate, a.review)
    elif a.action == 'select': result = select(a.episode, a.candidate, a.reason)
    elif a.action == 'extract': result = str(extract_atom(a.episode, a.design))
    else:
        result = []
        for path in sorted((a.state / 'atoms').glob('*.json')):
            try:
                atom = load_atom(path); result.append({'path': str(path), 'atom_id': atom['atom_id'], 'config': atom['config']})
            except (ValueError, KeyError, OSError) as error:
                result.append({'path': str(path), 'status': 'excluded_stale', 'reason': str(error)})
    print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__': main()
