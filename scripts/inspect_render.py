"""Rasterize PDF for human/agent inspection. Rendering alone is not visual approval."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from tablelib import sha256, write_json

def render(pdf: Path, output: Path, dpi: int=150) -> dict:
    if output.exists(): raise ValueError('Use fresh output directory')
    exe=shutil.which('pdftoppm')
    if not exe: return {'status':'unavailable','reason':'pdftoppm not on PATH'}
    if not 72<=dpi<=600: raise ValueError('DPI must be 72..600')
    output.mkdir(parents=True)
    p=subprocess.run([exe,'-png','-r',str(dpi),str(pdf.resolve()),str((output/'page').resolve())],capture_output=True,timeout=90)
    pages=sorted(output.glob('page-*.png'))
    result={'status':'rendered' if p.returncode==0 and pages else 'failed','returncode':p.returncode,'pdf_sha256':sha256(pdf),'dpi':dpi,'pages':[str(x.resolve()) for x in pages],'visual_review':'pending','stderr':p.stderr.decode('utf-8',errors='replace')}
    write_json(output/'render-report.json',result); return result

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('pdf',type=Path); p.add_argument('--output',required=True,type=Path); p.add_argument('--dpi',default=150,type=int)
    a=p.parse_args(); result=render(a.pdf,a.output,a.dpi); print(json.dumps(result,indent=2)); return 0 if result['status']=='rendered' else 2

if __name__=='__main__': raise SystemExit(main())
