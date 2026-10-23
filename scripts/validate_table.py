"""Heuristic static checking plus optional deterministic data-to-TeX verification."""
import argparse
import json
from pathlib import Path
from tablelib import generate, read_json, static_check, write_json

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path); p.add_argument('--spec',type=Path)
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    text=a.source.read_text(encoding='utf-8-sig')
    result=static_check(text)
    if a.spec:
        same=text==generate(read_json(a.spec))
        result['numerical_integrity']='verified_against_deterministic_generation' if same else 'unverified_source_differs_from_contract_render'
        if not same:
            result['errors'].append('Source does not match contract renderer; semantic ledger mapping required for arbitrary TeX')
            result['status']='fail'
    if a.report: write_json(a.report,result)
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return 1 if result['errors'] else 2 if result['unsupported'] else 0

if __name__=='__main__': raise SystemExit(main())
