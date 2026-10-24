"""Integration checks for the transcribe_table.generate ledger interface."""
import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_transcriber():
    spec = importlib.util.spec_from_file_location(
        'transcribe_table', ROOT / 'scripts' / 'transcribe_table.py'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coverage_ledger(symbols):
    return {
        'columns': [{'id': symbol, 'label': symbol.title()} for symbol in symbols],
        'rows': [{
            'id': 'row',
            'cells': {
                symbol: {'status': 'read', 'symbol': symbol}
                for symbol in symbols
            },
        }],
        'caption': 'Coverage symbols',
    }


class CoverageGeometryTest(unittest.TestCase):
    def test_generate_uses_equal_extents_and_distinct_fills(self):
        tex, unresolved = load_transcriber().generate(
            coverage_ledger(['full', 'half', 'empty'])
        )
        self.assertIsInstance(tex, str)
        self.assertEqual(unresolved, [])
        pictures = re.findall(
            r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', tex, re.DOTALL
        )
        self.assertEqual(len(pictures), 3)
        bounds = r'(-.89ex,-.89ex) rectangle (.89ex,.89ex)'
        for picture in pictures:
            self.assertIn(bounds, picture)
            self.assertIn('baseline=-.5ex', picture)
            self.assertIn('radius=.78ex', picture)
        self.assertIn('fill=black', pictures[0])
        self.assertIn('arc[start angle=90,end angle=270,radius=.78ex]', pictures[1])
        self.assertIn('fill=none', pictures[2])

    def test_generate_rejects_unknown_coverage_symbol(self):
        with self.assertRaises(ValueError):
            load_transcriber().generate(coverage_ledger(['unknown']))


if __name__ == '__main__':
    unittest.main()
