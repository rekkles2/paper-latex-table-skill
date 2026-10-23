import json
import sys
import tempfile
import unittest
from pathlib import Path

CANDIDATE = Path(sys.argv[sys.argv.index('--candidate') + 1]) if '--candidate' in sys.argv else Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CANDIDATE / 'scripts'))
from rsi_episode import start, candidate, review, select, extract_atom, load_atom, digest, CHECKS
from tablelib import sha256
from compose_designs import compose, verify, build, RECIPES
from tablelib import read_json, write_json


class EpisodeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.tex = self.root / 'table.tex'; self.tex.write_text('Editable table', encoding='utf-8')
        self.png = self.root / 'reference.png'; self.png.write_bytes(b'Image snapshot fixture')
        self.req = self.root / 'requirements.json'
        write_json(self.req, {'goal': 'Readable two-column table', 'constraints': {'target_width_mm': 90, 'min_font_pt': 8, 'font_pt': 10}})
        self.recipe = self.root / 'recipe.json'; write_json(self.recipe, {'parents': ['case@1'], 'reason': 'Preserve grouping at publication width', 'tabcolsep_pt': 4, 'arraystretch': 1.1, 'group_weight': 'bold-italic'})
        self.episode = start(self.root / 'state', 'paired', [self.tex, self.png], self.req)

    def tearDown(self): self.tmp.cleanup()

    def add(self):
        return candidate(self.episode, self.tex, [self.png], self.recipe)

    def review_file(self, folder, status='passed'):
        item = read_json(folder / 'candidate.json'); entry = read_json(self.episode / 'episode.json')
        evidence = item['artifacts'][-1]['path']
        data = {'candidate_hash': item['candidate_hash'], 'input_hash': entry['input_hash'], 'reviewer': 'unit-test-fixture',
                'review_type': 'self_review', 'unresolved_semantic_cells': 0,
                'checks': {c: {'status': status, 'evidence': [evidence]} for c in (*CHECKS, 'source_conflicts')}}
        path = self.root / 'review.json'; write_json(path, data)
        return path

    def test_paired_requires_both_modalities(self):
        with self.assertRaises(ValueError): start(self.root / 'other', 'paired', [self.tex], self.req)

    def test_image_only_requires_its_transcription_review(self):
        self.episode = start(self.root / 'image-state', 'image-only', [self.png], self.req)
        folder = self.add()
        with self.assertRaises(ValueError): review(self.episode, folder.name, self.review_file(folder))

    def test_reuse_selection_requires_baseline_comparison(self):
        self.episode = start(self.root / 'reuse-state', 'reuse', [self.tex], self.req)
        folder = self.add(); review(self.episode, folder.name, self.review_file(folder))
        with self.assertRaises(ValueError): select(self.episode, folder.name, 'Looks good')

    def test_tampered_snapshot_blocks_new_candidate(self):
        next((self.episode / 'inputs').glob('*table.tex')).write_text('changed')
        with self.assertRaises(ValueError): self.add()

    def test_three_candidate_budget(self):
        for _ in range(3): self.add()
        with self.assertRaises(ValueError): self.add()

    def test_pending_checks_never_select(self):
        folder = self.add(); result = review(self.episode, folder.name, self.review_file(folder, 'pending'))
        self.assertFalse(result['local_reuse_eligible'])
        with self.assertRaises(ValueError): select(self.episode, folder.name, 'No data changes')

    def test_review_hash_binding(self):
        folder = self.add(); path = self.review_file(folder); data = read_json(path)
        data['candidate_hash'] = 'unrelated'; write_json(path, data)
        with self.assertRaises(ValueError): review(self.episode, folder.name, path)

    def test_updated_file_hash_cannot_reuse_old_manifest_digest(self):
        folder = self.add(); path = self.review_file(folder)
        metadata = read_json(folder / 'candidate.json')
        artifact = folder / 'artifacts' / metadata['artifacts'][0]['path']
        artifact.write_text('changed candidate'); metadata['artifacts'][0]['sha256'] = sha256(artifact)
        write_json(folder / 'candidate.json', metadata)
        with self.assertRaises(ValueError): review(self.episode, folder.name, path)

    def test_unreviewed_atom_parameters_rejected(self):
        folder = self.add(); review(self.episode, folder.name, self.review_file(folder))
        select(self.episode, folder.name, 'All checks passed in this fixture')
        design = self.root / 'style.json'
        write_json(design, {'tabcolsep_pt': 10, 'arraystretch': 1.1, 'group_weight': 'italic'})
        with self.assertRaises(ValueError): extract_atom(self.episode, design)

    def test_replaced_inputs_cannot_reuse_old_review(self):
        folder = self.add(); review(self.episode, folder.name, self.review_file(folder))
        select(self.episode, folder.name, 'Actual review fixture')
        design = self.root / 'style.json'
        write_json(design, {'tabcolsep_pt': 4, 'arraystretch': 1.1, 'group_weight': 'bold-italic'})
        atom = extract_atom(self.episode, design)
        entry = read_json(self.episode / 'episode.json')
        p = self.episode / 'inputs' / entry['sources'][0]['path']; p.write_text('different input')
        entry['sources'][0]['sha256'] = sha256(p); entry['input_hash'] = digest(entry['sources'])
        write_json(self.episode / 'episode.json', entry)
        with self.assertRaises(ValueError): load_atom(atom)
        with self.assertRaises(ValueError): extract_atom(self.episode, design)

    def test_unresolved_transcription_blocks_reuse(self):
        folder = self.add(); path = self.review_file(folder); data = read_json(path)
        data['unresolved_semantic_cells'] = 1; write_json(path, data)
        self.assertFalse(review(self.episode, folder.name, path)['local_reuse_eligible'])

    def test_local_reuse_without_global_promotion(self):
        folder = self.add(); review(self.episode, folder.name, self.review_file(folder))
        result = select(self.episode, folder.name, 'All recorded user constraints met')
        self.assertFalse(result['stable_files_changed'])
        design = self.root / 'style.json'
        write_json(design, {'tabcolsep_pt': 4, 'arraystretch': 1.1, 'group_weight': 'bold-italic'})
        atom = extract_atom(self.episode, design)
        self.assertEqual(load_atom(atom)['config']['tabcolsep_pt'], 4)
        saved = atom.read_bytes(); altered = read_json(atom); altered['config']['tabcolsep_pt'] = 9
        write_json(atom, altered)
        with self.assertRaises(ValueError): load_atom(atom)
        atom.write_bytes(saved)
        (folder / 'artifacts' / read_json(folder / 'candidate.json')['artifacts'][0]['path']).write_text('new TeX')
        with self.assertRaises(ValueError): load_atom(atom)


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.spec = CANDIDATE / 'assets/templates/benchmark.json'
        self.req = self.root / 'requirements.json'
        write_json(self.req, {'goal': 'Compare same data', 'constraints': {'target_width_mm': 170, 'min_font_pt': 9, 'font_pt': 10}})

    def tearDown(self): self.tmp.cleanup()

    def test_all_compositions_keep_exact_contract(self):
        output = self.root / 'layouts'; items = compose(self.spec, self.req, output)
        self.assertEqual(len(items), 3)
        for item in items:
            self.assertEqual(verify(output / item['candidate'])['status'], 'passed')

    def test_editing_a_numeric_cell_invalidates_composition(self):
        output = self.root / 'layouts'; compose(self.spec, self.req, output)
        p = output / 'baseline/table.tex'; p.write_text(p.read_text().replace('81.20', '99.99'))
        with self.assertRaises(ValueError): verify(p.parent)

    def test_minimum_physical_font_is_hard_constraint(self):
        with self.assertRaises(ValueError): build(read_json(self.spec), RECIPES['baseline'], {'target_width_mm': 90, 'font_pt': 7, 'min_font_pt': 9})

    def test_deep_headers_are_not_claimed_supported(self):
        with self.assertRaises(ValueError): build(read_json(self.spec), RECIPES['baseline'], {'target_width_mm': 90, 'header_layers': 2})

    def test_font_is_inside_float_after_reset(self):
        tex = build(read_json(self.spec), RECIPES['baseline'], {'target_width_mm': 90, 'font_pt': 11})
        self.assertGreater(tex.index(r'\fontsize{11}'), tex.index(r'\begin{table}'))


if __name__ == '__main__': unittest.main()
