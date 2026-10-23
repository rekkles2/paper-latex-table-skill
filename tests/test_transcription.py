import copy
import sys
import unittest
from pathlib import Path

CANDIDATE = Path(sys.argv[sys.argv.index('--candidate') + 1]) if '--candidate' in sys.argv else Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CANDIDATE / 'scripts'))
from transcribe_table import generate


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.ledger = {'columns': [{'id': 'model', 'label': 'Model'}, {'id': 'value', 'label': 'Accuracy (%)'}],
                       'rows': [{'id': 'method-a', 'cells': {'model': {'status': 'read', 'text': 'A_B & C'},
                                'value': {'status': 'read', 'text': '81.00'}}}]}

    def test_exact_strings_and_escaping(self):
        tex, unresolved = generate(self.ledger)
        self.assertIn(r'A\_B \& C & 81.00', tex)
        self.assertIn(r'Accuracy (\%)', tex)
        self.assertEqual(unresolved, [])

    def test_ambiguous_digit_never_guessed(self):
        self.ledger['rows'][0]['cells']['value'] = {'status': 'ambiguous', 'text': '81.00', 'alternatives': ['81.00', '87.00']}
        tex, unresolved = generate(self.ledger)
        self.assertIn('[?]', tex)
        self.assertNotIn('81.00', tex)
        self.assertEqual(unresolved[0]['column'], 'value')

    def test_missing_column_cannot_silently_shift(self):
        del self.ledger['rows'][0]['cells']['value']
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_duplicate_identity_rejected(self):
        self.ledger['rows'].append(copy.deepcopy(self.ledger['rows'][0]))
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_unknown_symbol_rejected(self):
        self.ledger['rows'][0]['cells']['value'] = {'status': 'read', 'symbol': 'three-quarters'}
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_combined_typography_is_preserved(self):
        cell = self.ledger['rows'][0]['cells']['value']
        cell.update(bold=True, italic=True, underline=True)
        tex, _ = generate(self.ledger)
        self.assertIn(r'\underline{\textbf{\textit{81.00}}}', tex)

    def test_invalid_style_flag_is_not_silently_accepted(self):
        self.ledger['rows'][0]['cells']['value']['italic'] = 'yes'
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_header_spans_cover_grid(self):
        self.ledger['header_groups'] = [{'label': 'Scores', 'span': 3}]
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_cell_cannot_silently_choose_symbol_over_number(self):
        self.ledger['rows'][0]['cells']['value']['symbol'] = 'full'
        with self.assertRaises(ValueError): generate(self.ledger)

    def test_fractional_header_span_is_rejected(self):
        self.ledger['header_groups'] = [{'label': 'A', 'span': .5}, {'label': 'B', 'span': 1.5}]
        with self.assertRaises(ValueError): generate(self.ledger)


if __name__ == '__main__': unittest.main()
