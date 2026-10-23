"""Generate from an explicit JSON contract; refuse overwrites."""
import argparse
from pathlib import Path
from tablelib import generate, ledger, read_json, sha256, write_json

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec',type=Path); p.add_argument('output',type=Path)
    a=p.parse_args()
    spec=read_json(a.spec)
    text=generate(spec)
    receipt=a.output.with_suffix('.ledger.json')
    if a.output.exists() or receipt.exists():
        p.error('Output or ledger already exists; choose a new path')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(text,encoding='utf-8')
    write_json(receipt,{'data':ledger(spec),'source_sha256':sha256(a.spec),'tex_sha256':sha256(a.output),'rank_policy':'dense-distinct-per-group; exact Decimal; mean only by explicit opt-in'})
    print(a.output)

if __name__=='__main__': main()
