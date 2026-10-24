"""Allowlist a portable skill and root docs into a new ZIP; omit local references."""
import argparse
import json
import zipfile
from pathlib import Path
from tablelib import ROOT, sha256, read_json

def public_markdown(text: str) -> str:
    """Strip explicitly marked local-only blocks; fail closed on malformed markers."""
    from gallery_export import check_private_links
    begin='<!-- LOCAL-ONLY:BEGIN -->';end='<!-- LOCAL-ONLY:END -->'
    out=[];inside=False
    for line in text.splitlines(keepends=True):
        if begin in line:
            if inside or line.strip()!=begin: raise ValueError('Malformed or nested local-only block')
            inside=True
        elif end in line:
            if not inside or line.strip()!=end: raise ValueError('Unmatched local-only end')
            inside=False
        elif not inside:out.append(line)
    if inside:raise ValueError('Unclosed local-only block')
    cleaned=''.join(out)
    import re
    if re.search(r'(?:\]\([^)]*|(?:src|href)=[\x22\x27][^\x22\x27]*)assets/cases/local/',cleaned):
        raise ValueError('Private link outside a local-only block')
    return check_private_links(cleaned)


def export(output: Path) -> list[dict]:
    from gallery_export import enhance_entries
    entries={}
    extensions={'agents':{'.yaml'},'references':{'.md'},'scripts':{'.py'},'tests':{'.py'},'rsi':{'.md'},'rsi/templates':{'.json'},'assets/templates':{'.json','.tex'}}
    for directory in ('agents','references','scripts','tests','rsi','rsi/templates','assets/templates'):
        for p in (ROOT/directory).rglob('*'):
            relative=p.relative_to(ROOT)
            if p.is_file() and p.suffix in extensions[directory] and not any(part.startswith('.') or part=='__pycache__' for part in relative.parts):
                if not p.resolve().is_relative_to((ROOT/directory).resolve()):
                    raise ValueError('Export source resolves outside allowed directory')
                entries['paper-latex-table-skill/'+p.relative_to(ROOT).as_posix()]=public_markdown(p.read_text(encoding='utf-8')).encode('utf-8') if p.suffix=='.md' else p.read_bytes()
    entries['paper-latex-table-skill/SKILL.md']=public_markdown((ROOT/'SKILL.md').read_text(encoding='utf-8')).encode('utf-8')
    # A skill can also be the repository root. Keep its README-relative media
    # together when exporting instead of relying on parent-repository files.
    for p in (ROOT/'docs').rglob('*'):
        relative=p.relative_to(ROOT)
        if p.is_file() and p.suffix in {'.md','.txt','.json','.tex','.png','.py'} and not any(part.startswith('.') or part=='__pycache__' for part in relative.parts):
            if not p.resolve().is_relative_to((ROOT/'docs').resolve()):
                raise ValueError('Documentation resolves outside docs directory')
            entries['paper-latex-table-skill/'+relative.as_posix()]=public_markdown(p.read_text(encoding='utf-8')).encode('utf-8') if p.suffix=='.md' else p.read_bytes()
    public=[]
    for meta in (ROOT/'assets'/'cases'/'public').glob('*/case.json'):
        record=read_json(meta)
        if record.get('rights')!='original-project-example': raise ValueError('Unknown case rights')
        for source in record['sources']:
            p=(meta.parent/source['path']).resolve()
            if not p.is_relative_to(meta.parent.resolve()) or sha256(p)!=source['sha256']: raise ValueError('Invalid public source')
            entries['paper-latex-table-skill/'+p.relative_to(ROOT).as_posix()]=p.read_bytes()
        entries['paper-latex-table-skill/'+meta.relative_to(ROOT).as_posix()]=meta.read_bytes()
        record['metadata_path']=meta.relative_to(ROOT/'assets'/'cases').as_posix(); public.append(record)
    entries['paper-latex-table-skill/assets/case-index.json']=json.dumps({'schema_version':1,'cases':public},indent=2).encode()
    for name in ('README.md','README.en.md','LICENSE','.gitignore'):
        local=ROOT/name
        if local.is_file():
            entries['paper-latex-table-skill/'+name]=public_markdown(local.read_text(encoding='utf-8')).encode('utf-8') if name.endswith('.md') else local.read_bytes()
            if name=='README.md':
                entries[name]=b'# Paper LaTeX Table Skill\n\nRead the [illustrated README and installation guide](paper-latex-table-skill/README.md).\n'
            elif name != 'README.en.md':
                entries[name]=local.read_bytes()
        else:
            if name != 'README.en.md':
                entries[name]=(ROOT.parent/name).read_bytes()
    forbidden={sha256(p) for p in (ROOT/'assets'/'cases'/'local').rglob('*') if p.is_file()}
    import hashlib
    entries = enhance_entries(entries, ROOT)
    manifest=[]
    for name,data in sorted(entries.items()):
        digest=hashlib.sha256(data).hexdigest()
        if digest in forbidden: raise ValueError('Local reference leaked: '+name)
        manifest.append({'path':name,'sha256':digest,'provenance':'project-authored','license':'see LICENSE; project license pending'})
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(entries.items()): z.writestr(name,data)
        z.writestr('release-manifest.json',json.dumps(manifest,indent=2))
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('output',type=Path); a=p.parse_args(); print(f'Exported {len(export(a.output))} files')
