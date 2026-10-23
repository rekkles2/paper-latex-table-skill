"""Append-only RSI records; never edits stable skill files or auto-promotes cases."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from tablelib import ROOT, read_json, sha256, write_json

def tree_hash(root: Path) -> str:
    h=hashlib.sha256()
    for path in sorted(root.rglob('*')):
        if path.is_file() and not any(p in ('__pycache__','.git','.local','state','skill-state','build') for p in path.relative_to(root).parts):
            h.update(path.relative_to(root).as_posix().encode()); h.update(bytes.fromhex(sha256(path)))
    return h.hexdigest()

def propose(candidate: Path, state: Path, reason: str, case: str) -> Path:
    candidate=candidate.resolve(); state=state.resolve()
    if state.is_relative_to(candidate):
        raise ValueError('State must be outside candidate tree')
    if state.is_relative_to(ROOT.resolve()):
        raise ValueError('State must be outside stable skill tree (avoids recursive snapshots)')
    if not (candidate/'SKILL.md').exists() or not (candidate/'tests'/'test_tables.py').exists():
        raise ValueError('Candidate must be a complete skill tree with regression suite')
    digest=tree_hash(candidate)
    folder=state/digest
    folder.mkdir(parents=True,exist_ok=False)
    # A rollback snapshot of the stable skill, not a destructive installation.
    with zipfile.ZipFile(folder/'baseline.zip','x',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ROOT.rglob('*')):
            if f.is_file() and not any(x in ('__pycache__','.git','.local','state','skill-state','build') for x in f.relative_to(ROOT).parts):
                z.write(f,f.relative_to(ROOT))
    write_json(folder/'proposal.json',{'candidate':str(candidate),'candidate_hash':digest,'baseline_hash':tree_hash(ROOT),'reason':reason,'case':case,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'pending'})
    return folder

def evaluate(folder: Path) -> dict:
    if (folder/'evaluation.json').exists(): raise ValueError('Evaluation is append-only; create a new proposal for changed candidates')
    proposal=read_json(folder/'proposal.json'); candidate=Path(proposal['candidate'])
    if tree_hash(candidate)!=proposal['candidate_hash']: raise ValueError('Candidate changed')
    # Execute the maintained stable test harness against candidate modules.
    # Candidate code is executable; evaluate only user-authorized local candidates.
    cmd=[sys.executable,'-B',str(ROOT/'tests'/'run_regressions.py'),'--candidate',str(candidate)]
    result=subprocess.run(cmd,capture_output=True,timeout=180)
    log=folder/'tests.log'; log.write_bytes(result.stdout+result.stderr)
    evidence={'status':'passed' if result.returncode==0 else 'failed','returncode':result.returncode,'command':cmd,'tests_sha256':sha256(log),'harness_sha256':tree_hash(ROOT/'tests'),'candidate_hash':tree_hash(candidate),'baseline_hash':tree_hash(ROOT)}
    write_json(folder/'evaluation.json',evidence); return evidence

def accept(folder: Path, approver: str, approval: str, visual: Path) -> dict:
    if not approver.strip() or not approval.strip(): raise ValueError('Explicit approver and approval text required')
    if (folder/'acceptance.json').exists(): raise ValueError('Acceptance already recorded')
    p=read_json(folder/'proposal.json'); e=read_json(folder/'evaluation.json')
    if e['status']!='passed' or e['returncode']!=0: raise ValueError('Regression failed')
    if e['candidate_hash']!=p['candidate_hash'] or tree_hash(Path(p['candidate']))!=p['candidate_hash']: raise ValueError('Stale candidate')
    if tree_hash(ROOT)!=p['baseline_hash'] or e['baseline_hash']!=p['baseline_hash']: raise ValueError('Stable baseline changed')
    if sha256(folder/'tests.log')!=e['tests_sha256'] or tree_hash(ROOT/'tests')!=e['harness_sha256']: raise ValueError('Evidence changed')
    v=read_json(visual)
    if v.get('candidate_hash')!=p['candidate_hash'] or v.get('status')!='passed' or not v.get('reviewer') or not v.get('artifacts'):
        raise ValueError('Need candidate-bound visual/compile review with artifact hashes')
    for artifact in v['artifacts']:
        if sha256((visual.parent/artifact['path']).resolve())!=artifact['sha256']: raise ValueError('Changed visual artifact')
    record={'status':'accepted_for_manual_integration','candidate_hash':p['candidate_hash'],'evaluation_sha256':sha256(folder/'evaluation.json'),'visual_sha256':sha256(visual),'approver':approver,'approval':approval,'accepted_utc':datetime.now(timezone.utc).isoformat()}
    write_json(folder/'acceptance.json',record); return record

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='action',required=True)
    q=sub.add_parser('propose'); q.add_argument('candidate',type=Path); q.add_argument('--state',required=True,type=Path); q.add_argument('--reason',required=True); q.add_argument('--case',required=True)
    q=sub.add_parser('evaluate'); q.add_argument('folder',type=Path)
    q=sub.add_parser('accept'); q.add_argument('folder',type=Path); q.add_argument('--approve-by',required=True); q.add_argument('--approval',required=True); q.add_argument('--visual-review',required=True,type=Path)
    a=p.parse_args()
    if a.action=='propose': print(propose(a.candidate,a.state,a.reason,a.case))
    elif a.action=='evaluate':
        result=evaluate(a.folder); print(json.dumps(result)); return 0 if result['status']=='passed' else 1
    else: print(json.dumps(accept(a.folder,a.approve_by,a.approval,a.visual_review)))
    return 0

if __name__=='__main__': raise SystemExit(main())
