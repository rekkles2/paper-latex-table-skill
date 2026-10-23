"""Compile a trusted TeX fragment or full document, with auditable exit/log status.

TeX is executable input: -no-shell-escape is defense in depth, not a sandbox.
Use an OS sandbox/container for unknown third-party TeX.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from tablelib import sha256, write_json

PREAMBLE=r'''\documentclass{article}
\usepackage[margin=22mm]{geometry}
\usepackage{booktabs,multirow,makecell,tabularx,adjustbox,siunitx,amsmath,amssymb}
\usepackage[table]{xcolor}
\listfiles
'''

def compile_source(source: Path, output: Path, engine: str='auto', preamble: Path|None=None, timeout: int=60) -> dict:
    if output.exists():
        raise ValueError('Compilation directory must be fresh (prevents stale-PDF success)')
    engines=('pdflatex','xelatex','lualatex','latexmk') if engine=='auto' else (engine,)
    executable=next((shutil.which(e) for e in engines if shutil.which(e)),None)
    if not executable:
        return {'status':'unavailable','reason':'No requested TeX engine on PATH','visual_review':'not_performed'}
    if timeout<1: raise ValueError('timeout must be positive')
    source=source.resolve()
    output.mkdir(parents=True)
    text=source.read_text(encoding='utf-8-sig')
    full=bool(re.search(r'\\documentclass(?:\[.*?\])?\{',text))
    # Full documents retain their own class/packages. Fragment wrappers may add supplied macros.
    wrapper=text if full else PREAMBLE+(preamble.read_text(encoding='utf-8-sig') if preamble else '')+'\n\\begin{document}\n'+text+'\n\\end{document}\n'
    job=output/'table-build.tex'; job.write_text(wrapper,encoding='utf-8')
    cmd=[executable]
    if Path(executable).stem.lower()=='latexmk': cmd+=['-pdf']
    cmd+=['-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error',f'-output-directory={output.resolve()}',str(job.resolve())]
    result={'source_sha256':sha256(source),'preamble_sha256':sha256(preamble) if preamble and not full else None,'wrapper_sha256':sha256(job),'engine':executable,'command':cmd,'source_mode':'full_document' if full else 'generic_article_fragment','visual_review':'not_performed','runs':[]}
    try:
        for _ in range(2):
            process=subprocess.run(cmd,cwd=source.parent,capture_output=True,timeout=timeout)
            result['runs'].append({'returncode':process.returncode,'stdout':process.stdout.decode('utf-8',errors='replace'),'stderr':process.stderr.decode('utf-8',errors='replace')})
            if process.returncode: break
        log=(output/'table-build.log').read_text(encoding='utf-8',errors='replace') if (output/'table-build.log').exists() else ''
        pdf=output/'table-build.pdf'
        fatal=bool(re.search(r'^!|Fatal error|Emergency stop|^[^\r\n]+:\d+:\s*(?![^\r\n]*\bWarning\b)\S',log,re.M))
        result.update(status='passed' if result['runs'][-1]['returncode']==0 and pdf.exists() and not fatal else 'failed',pdf=str(pdf.resolve()) if pdf.exists() else None)
        result['warnings']=[line for line in log.splitlines() if re.search(r'Overfull \\[hv]box|Underfull \\[hv]box|undefined|Missing character:|(?:LaTeX|Package \S+|Class \S+).*Warning:|Float too large',line,re.I)]
        result['layout_status']='needs_review' if result['warnings'] else 'no_log_warnings'
        result['log_sha256']=sha256(output/'table-build.log') if log else None
    except subprocess.TimeoutExpired:
        result.update(status='timeout',reason=f'Engine exceeded {timeout}s in a pass')
    write_json(output/'compile-report.json',result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path); p.add_argument('--output',required=True,type=Path)
    p.add_argument('--engine',choices=['auto','pdflatex','xelatex','lualatex','latexmk'],default='auto')
    p.add_argument('--preamble',type=Path); p.add_argument('--timeout',type=int,default=60)
    a=p.parse_args(); result=compile_source(a.source,a.output,a.engine,a.preamble,a.timeout)
    print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
    return 0 if result['status']=='passed' else 2 if result['status']=='unavailable' else 1

if __name__=='__main__': raise SystemExit(main())
