"""Compose at most three inspectable layout candidates from one immutable data spec.

This is deterministic design reuse, not an automatic beauty optimizer. Actual
compilation, typography, physical-width review and selection remain explicit.
"""
import argparse
import json
from pathlib import Path

from tablelib import generate, ledger, read_json, sha256, write_json
from rsi_episode import load_atom, validate_atom_config

RECIPES = {
    'baseline': {'tabcolsep_pt': 6, 'arraystretch': 1.0, 'group_weight': 'italic',
                 'parents': ['booktabs-base@1']},
    'grouped-readable': {'tabcolsep_pt': 5, 'arraystretch': 1.12, 'group_weight': 'bold-italic',
                         'parents': ['booktabs-base@1', 'group-hierarchy@1', 'roomy-rows@1']},
    'compact-readable': {'tabcolsep_pt': 3.5, 'arraystretch': 1.06, 'group_weight': 'italic',
                         'parents': ['booktabs-base@1', 'compact-spacing@1']},
}


def build(spec, recipe, constraints):
    validate_atom_config({k: recipe[k] for k in ('tabcolsep_pt', 'arraystretch', 'group_weight')})
    if constraints.get('header_layers', 1) > 1:
        raise ValueError('Deeper headers need agent-authored TeX and a checked cell ledger')
    minimum = constraints.get('min_font_pt', 8)
    font = constraints.get('font_pt', 10)
    width = constraints.get('target_width_mm')
    if not isinstance(minimum, (int, float)) or not isinstance(font, (int, float)) or not 6 <= minimum <= font <= 24:
        raise ValueError('Declare sensible font_pt >= min_font_pt; never shrink below it')
    if not isinstance(width, (int, float)) or not 40 <= width <= 500:
        raise ValueError('Declare a physical target_width_mm between 40 and 500')
    body = generate(spec)
    if recipe['group_weight'] == 'bold-italic':
        # Only renderer-owned group-label lines can receive this hierarchy style.
        lines = body.splitlines()
        for i, line in enumerate(lines):
            if line.startswith(r'\multicolumn{') and r'{l}{\textit{' in line:
                lines[i] = line.replace(r'{l}{\textit{', r'{l}{\bfseries\textit{', 1)
        body = '\n'.join(lines) + '\n'
    settings = ('\\fontsize{%s}{%s}\\selectfont\n' % (font, font * 1.2)
              + '\\setlength{\\tabcolsep}{%spt}\n' % recipe['tabcolsep_pt']
              + '\\renewcommand{\\arraystretch}{%s}\n' % recipe['arraystretch'])
    # Float construction resets to normalsize, so apply settings inside it.
    body = body.replace('\\centering\n', '\\centering\n' + settings, 1)
    return '\\begingroup\n' + body + '\\endgroup\n'


def compose(spec_path, requirements_path, output, atom_paths=()):
    if output.exists(): raise ValueError('Use a fresh candidate directory')
    spec = read_json(spec_path); req = read_json(requirements_path)
    constraints = req['constraints']
    # Validate all candidates before producing any artifact.
    if len(atom_paths) > 2: raise ValueError('At most two learned atoms plus the baseline')
    recipes = dict(RECIPES)
    if atom_paths:
        recipes = {'baseline': RECIPES['baseline']}
        for path in atom_paths:
            atom = load_atom(path)
            recipes['learned-' + atom['atom_id']] = dict(atom['config'], parents=[atom['atom_id'] + '@' + str(atom['version'])], atom_sha256=sha256(path))
    rendered = {name: build(spec, recipe, constraints) for name, recipe in recipes.items()}
    output.mkdir(parents=True)
    write_json(output / 'spec.json', spec); write_json(output / 'requirements.json', req)
    summary = []
    for name, text in rendered.items():
        folder = output / name; folder.mkdir()
        tex = folder / 'table.tex'; tex.write_text(text, encoding='utf-8')
        recipe = dict(recipes[name], reason='Compare readable grouping and spacing at the same physical font size; data and metric scopes unchanged.')
        write_json(folder / 'recipe.json', recipe)
        write_json(folder / 'receipt.json', {'source_sha256': sha256(spec_path), 'spec_snapshot_sha256': sha256(output / 'spec.json'),
                   'requirements_snapshot_sha256': sha256(output / 'requirements.json'), 'tex_sha256': sha256(tex),
                   'recipe_sha256': sha256(folder / 'recipe.json'), 'data': ledger(spec),
                   'status': 'generated_unreviewed', 'geometry': 'target width is a constraint, not a measured fit result'})
        summary.append({'candidate': name, 'atoms': recipe['parents'], 'target_width_mm': constraints['target_width_mm'],
                        'verification': 'compile and inspect at target size before selection'})
    write_json(output / 'plan.json', {'candidates': summary, 'selection': 'pending; no beauty score or automatic winner'})
    return summary


def verify(folder):
    receipt = read_json(folder / 'receipt.json'); spec = folder.parent / 'spec.json'
    req = folder.parent / 'requirements.json'; recipe_path = folder / 'recipe.json'; tex = folder / 'table.tex'
    if any(sha256(path) != receipt[key] for path, key in [(spec, 'spec_snapshot_sha256'), (req, 'requirements_snapshot_sha256'),
            (recipe_path, 'recipe_sha256'), (tex, 'tex_sha256')]):
        raise ValueError('Candidate or its source/design evidence changed')
    expected = build(read_json(spec), read_json(recipe_path), read_json(req)['constraints'])
    if tex.read_text(encoding='utf-8') != expected or ledger(read_json(spec)) != receipt['data']:
        raise ValueError('Candidate differs from its deterministic composition or data contract')
    return {'status': 'passed', 'data': 'exact deterministic composition verified', 'visual': 'pending'}


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='action', required=True)
    q = sub.add_parser('generate'); q.add_argument('spec', type=Path); q.add_argument('--requirements', type=Path, required=True); q.add_argument('--output', type=Path, required=True)
    q.add_argument('--atom', type=Path, action='append', default=[])
    q = sub.add_parser('verify'); q.add_argument('candidate', type=Path)
    a = p.parse_args()
    result = compose(a.spec, a.requirements, a.output, a.atom) if a.action == 'generate' else verify(a.candidate)
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
