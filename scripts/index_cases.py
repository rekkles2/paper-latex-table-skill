"""Index explicit case metadata, verifying all stored source hashes."""
import argparse
from pathlib import Path
from tablelib import ROOT, read_json, sha256, write_json

def build_index(root: Path) -> list[dict]:
    cases=[]
    for meta in sorted(root.rglob('case.json')):
        case=read_json(meta)
        for source in case['sources']:
            path=(meta.parent/source['path']).resolve()
            if not path.is_relative_to(meta.parent.resolve()):
                raise ValueError('Source outside case folder')
            if sha256(path)!=source['sha256']:
                raise ValueError('Source changed: '+str(path))
        case['metadata_path']=meta.relative_to(root).as_posix()
        cases.append(case)
    if len({c['case_id'] for c in cases})!=len(cases):
        raise ValueError('Duplicate case IDs')
    return cases

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cases',type=Path,default=ROOT/'assets'/'cases')
    p.add_argument('--output',type=Path,default=ROOT/'assets'/'case-index.json')
    a=p.parse_args(); cases=build_index(a.cases)
    write_json(a.output,{'schema_version':1,'cases':cases})
    print(f'Indexed {len(cases)} cases')

if __name__=='__main__': main()
