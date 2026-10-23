"""Maintained harness; execute stable tests against candidate modules, not its tests."""
import argparse
from pathlib import Path
import sys
import unittest

p = argparse.ArgumentParser(); p.add_argument('--candidate', type=Path, required=True)
a = p.parse_args()
sys.path.insert(0, str(a.candidate.resolve() / 'scripts'))
suite = unittest.TestLoader().discover(str(Path(__file__).resolve().parent), pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
