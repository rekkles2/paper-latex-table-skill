import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

CANDIDATE = Path(sys.argv[sys.argv.index('--candidate') + 1]) if '--candidate' in sys.argv else Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CANDIDATE / 'scripts'))
from reproduce_case import reproduce
from tablelib import sha256


class ReproductionTests(unittest.TestCase):
    def make_case(self, root):
        case = root / 'case'; profile = case / 'reproduction'; profile.mkdir(parents=True)
        source = case / 'table.tex'; source.write_text(r'\begin{tabular}{c}81.00\\\end{tabular}')
        (case / 'case.json').write_text(json.dumps({'sources': [{'path': 'table.tex', 'sha256': sha256(source)}]}))
        (profile / 'macros.tex').write_text('')
        (profile / 'profile.json').write_text(json.dumps({'source': '../table.tex', 'macros': 'macros.tex', 'assets': [], 'width_mm': 100, 'height_mm': 100, 'case_id': 'fixture', 'engine': 'xelatex', 'notes': []}))
        return case

    def test_reproduction_does_not_write_inside_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); case = self.make_case(root)
            before = {p.relative_to(case).as_posix(): p.read_bytes() for p in case.rglob('*') if p.is_file()}
            with patch('reproduce_case.compile_source', return_value={'status': 'failed'}): reproduce(case, root / 'out')
            after = {p.relative_to(case).as_posix(): p.read_bytes() for p in case.rglob('*') if p.is_file()}
            self.assertEqual(before, after)
            self.assertTrue((root / 'out/work/document.tex').exists())

    def test_original_tampering_prevents_compile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); case = self.make_case(root)
            (case / 'table.tex').write_text('99.99')
            with patch('reproduce_case.compile_source') as compile_mock:
                with self.assertRaises(ValueError): reproduce(case, root / 'out')
                compile_mock.assert_not_called()
