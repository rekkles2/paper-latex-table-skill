"""Verify figure/TeX pair paths and hashes, not scientific or visual correctness."""
import argparse,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate(index:Path,root:Path=ROOT)->list[dict]:
 data=json.loads(index.read_text(encoding='utf8'));seen=set();rows=[]
 for item in data['examples']:
  if item['id'] in seen:raise ValueError('Duplicate example ID: '+item['id'])
  seen.add(item['id'])
  for field in ('figure','tex'):
   rel=Path(item[field]);p=(root/rel).resolve()
   if rel.is_absolute() or not p.is_relative_to(root.resolve()):raise ValueError('Path outside skill: '+str(rel))
   if not p.is_file():raise ValueError('Missing '+field+': '+str(rel))
   expected=item['sha256'][field]
   if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('Changed '+field+': '+str(rel))
  rows.append({'id':item['id'],'pair':'present_and_hash_matched','scientific_verification':'not_established_by_hashes'})
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private',action='store_true');a=p.parse_args()
 indexes=[ROOT/'docs/gallery-public.json']
 if a.private:indexes.append(ROOT/'assets/cases/local/gallery-pairs.json')
 rows=[r for i in indexes for r in validate(i)]
 print(json.dumps({'status':'passed','pairs':len(rows),'examples':rows},indent=2))
