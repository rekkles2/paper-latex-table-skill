"""Persist private candidate cases/feedback. Never changes stable rules or cases."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import uuid
from tablelib import ROOT, sha256, write_json

def default_state() -> Path:
    home=Path(os.environ['CODEX_HOME']) if os.environ.get('CODEX_HOME') else Path.home()/'.codex'
    return (home/'skill-state'/'paper-latex-table-skill').resolve()

def record(state: Path, *, kind: str, reason: str, sources: list[Path], evidence: list[Path]|None=None, case_id: str|None=None, columns: int|None=None, table_type: str='unclassified', features: list[str]|None=None) -> Path:
    state=state.resolve()
    if state.is_relative_to(ROOT.resolve()):
        raise ValueError('Learning state must be outside the stable skill tree')
    if kind not in ('case','feedback') or not reason.strip():
        raise ValueError('Use kind=case/feedback and a nonempty observation')
    if kind=='case' and not sources:
        raise ValueError('A candidate case needs at least one actual source')
    if columns is not None and columns<1:
        raise ValueError('columns must be positive')
    ident=case_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:10]
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,95}',ident):
        # Generated timestamp is lowercase for the same portable case-ID contract.
        if case_id is not None: raise ValueError('ID must be lowercase letters, digits and hyphens')
        ident=ident.lower()
    files=[(Path(p).resolve(),Path(p).name,'source') for p in sources]
    files += [(Path(p).resolve(),'evidence-'+Path(p).name,'evidence') for p in (evidence or [])]
    names=[name for _,name,_ in files]
    if len(set(names))!=len(names) or any(name in ('case.json','record.json') for name in names):
        raise ValueError('Input filenames collide; rename source copies before recording')
    for path,_,_ in files:
        if not path.is_file(): raise ValueError('Missing input: '+str(path))
    folder=state/'candidates'/('cases' if kind=='case' else 'feedback')/ident
    folder.mkdir(parents=True,exist_ok=False)
    source_records=[]; evidence_records=[]
    for source,name,role in files:
        target=folder/name
        before=sha256(source)
        shutil.copyfile(source,target)
        if sha256(target)!=before: raise ValueError('Source changed while recording: '+str(source))
        item={'path':name,'sha256':before,'original_path':str(source)}
        (source_records if role=='source' else evidence_records).append(item)
    entry={'schema_version':1,'case_id':ident,'kind':kind,'reason':reason,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'pending','verified':False,'rights':'unknown-local-only','provenance':'Observed during an authorized table task; not automatically verified or licensed','source_type':'task_candidate','table_type':table_type,'columns':columns,'features':sorted(set(features or [])),'sources':source_records,'evidence':evidence_records,'compilation':'not_adjudicated','visual_status':'not_adjudicated','promotion':'requires verification and explicit approval; no stable files modified'}
    write_json(folder/('case.json' if kind=='case' else 'record.json'),entry)
    return folder

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state',type=Path,default=default_state())
    p.add_argument('--kind',choices=['case','feedback'],required=True)
    p.add_argument('--reason',required=True); p.add_argument('--source',type=Path,action='append',default=[])
    p.add_argument('--evidence',type=Path,action='append',default=[]); p.add_argument('--id')
    p.add_argument('--columns',type=int); p.add_argument('--type',default='unclassified')
    p.add_argument('--feature',action='append',default=[])
    a=p.parse_args()
    folder=record(a.state,kind=a.kind,reason=a.reason,sources=a.source,evidence=a.evidence,case_id=a.id,columns=a.columns,table_type=a.type,features=a.feature)
    print(json.dumps({'status':'pending','path':str(folder),'stable_files_changed':False},ensure_ascii=True)); return 0

if __name__=='__main__': raise SystemExit(main())
