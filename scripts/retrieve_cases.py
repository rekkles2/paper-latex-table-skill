"""Deterministic structural retrieval, with transparent scores."""
import argparse
import json
from pathlib import Path
from tablelib import ROOT, read_json, retrieve

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--index',type=Path,default=ROOT/'assets'/'case-index.json')
    p.add_argument('--columns',type=int); p.add_argument('--feature',action='append',default=[])
    p.add_argument('--type'); p.add_argument('--limit',type=int,default=5)
    a=p.parse_args()
    if a.limit<1 or (a.columns is not None and a.columns<1): p.error('Positive limit/columns required')
    print(json.dumps(retrieve(read_json(a.index)['cases'],columns=a.columns,features=a.feature,table_type=a.type,limit=a.limit),ensure_ascii=True,indent=2))

if __name__=='__main__': main()
