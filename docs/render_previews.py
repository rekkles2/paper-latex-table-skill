"""Rebuild README figures from original synthetic JSON and real LaTeX renders.

Documentation-only dependencies: Pillow, a TeX engine and Poppler/pdftoppm.
Run from the skill repository root, with a fresh --build-root.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from tablelib import generate, read_json, sha256, write_json
from compile_table import compile_source
from inspect_render import render

def column(cid: str, label: str, direction: str='higher', **kwargs) -> dict:
    return {'id':cid,'label':label,'direction':direction,**kwargs}

def save_source(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_text(encoding='utf-8')!=text:
        raise ValueError('Existing example differs; preserve/review it before rebuilding: '+str(path))
    if not path.exists(): path.write_text(text,encoding='utf-8')

def specifications() -> dict:
    benchmark={
        'schema_version':1,'caption':'Synthetic multi-dataset comparison. Bold: best; underline: second-best. Not measured experiments.','label':'tab:demo-benchmark',
        'columns':[
            column('a_auc','AUC',header_group='Dataset A',unit='%'),column('a_f1','F1',header_group='Dataset A',unit='%'),
            column('b_auc','AUC',header_group='Dataset B',unit='%'),column('b_f1','F1',header_group='Dataset B',unit='%'),
            column('latency','Latency','lower',header_group='Efficiency',unit='ms'),column('params','Params','none',header_group='Efficiency',kind='text')],
        'rows':[
            {'id':'baseline-a','label':'Baseline A','values':{'a_auc':'82.40','a_f1':'76.10','b_auc':'79.30','b_f1':'72.80','latency':'8.2','params':'8.1M'}},
            {'id':'baseline-b','label':'Baseline B','values':{'a_auc':'84.10','a_f1':'77.60','b_auc':'81.20','b_f1':'74.50','latency':'9.6','params':'8.8M'}},
            {'id':'memory','label':'Memory variant','values':{'a_auc':'86.30','a_f1':'79.20','b_auc':'83.10','b_f1':'76.40','latency':'10.4','params':'9.4M'}},
            {'id':'full','label':'Full model','values':{'a_auc':'86.30','a_f1':'80.50','b_auc':'84.60','b_f1':'77.90','latency':'11.1','params':'9.8M'}}]
    }
    # Explicit opt-in for rankings of means; uncertainty is not significance.
    ablation={'schema_version':1,'caption':'Synthetic component ablation (mean plus or minus standard deviation). Not measured experiments.','label':'tab:demo-ablation',
        'columns':[column('memory','Memory','none',kind='text'),column('rules','Rules','none',kind='text'),column('auc','AUC',unit='%',rank_on='mean'),column('f1','F1',unit='%',rank_on='mean')],
        'rows':[]}
    for rid,label,memory,rules,auc,std,f1,fstd in [
        ('base','Baseline','off','off','81.20','0.24','74.10','0.31'),
        ('memory','Memory only','on','off','83.60','0.21','76.30','0.28'),
        ('rules','Rules only','off','on','82.90','0.23','75.70','0.30'),
        ('full','Memory + rules','on','on','85.10','0.19','78.20','0.25')]:
        ablation['rows'].append({'id':rid,'label':label,'values':{'memory':memory,'rules':rules,'auc':{'mean':auc,'std':std},'f1':{'mean':f1,'std':fstd}}})
    return {'benchmark':benchmark,'ablation':ablation}

PREAMBLE=r'''\documentclass[10pt]{article}
\usepackage[paperwidth=190mm,paperheight=85mm,margin=8mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,booktabs,siunitx,amsmath}
\pagestyle{empty}
\renewcommand{\arraystretch}{1.20}
\setlength{\tabcolsep}{7pt}
\listfiles
\begin{document}
'''

def crop(path: Path) -> Image.Image:
    img=Image.open(path).convert('RGB')
    difference=ImageChops.difference(img,Image.new('RGB',img.size,'white')).convert('L')
    box=difference.point(lambda x:255 if x>20 else 0).getbbox()
    if not box: raise ValueError('Rendered page is empty')
    return ImageOps.expand(img.crop(box),border=26,fill='white')

def font(size: int):
    for name in ('DejaVuSans.ttf','arial.ttf'):
        try: return ImageFont.truetype(name,size)
        except OSError: pass
    return ImageFont.load_default()

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--build-root',required=True,type=Path)
    a=p.parse_args(); build=a.build_root.resolve()
    if build.exists(): p.error('Choose a fresh build root')
    build.mkdir(parents=True)
    examples=ROOT/'docs'/'examples'; images=ROOT/'docs'/'images'; images.mkdir(parents=True,exist_ok=True)
    specs=specifications(); tex={}
    for name,spec in specs.items():
        import json
        save_source(examples/(name+'.json'),json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
        tex[name]=generate(spec); save_source(examples/(name+'.tex'),tex[name])
    refined=tex['benchmark']
    before=refined.replace(r'\begin{tabular}{@{}lcccccc@{}}',r'\begin{tabular}{|l|c|c|c|c|c|c|}')
    before=before.replace(r'\toprule',r'\hline').replace(r'\midrule',r'\hline').replace(r'\bottomrule',r'\hline')
    import re
    before=re.sub(r'\\cmidrule\(lr\)\{(\d+-\d+)\}',r'\\cline{\1}',before)
    rows=[line for line in refined.splitlines() if '&' in line]
    assert all(line in before.splitlines() for line in rows)
    save_source(examples/'refinement-before.tex',before); save_source(examples/'refinement-after.tex',refined)
    tex['refinement-before']=before
    rendered={}; evidence=[]
    for name,fragment in tex.items():
        full=build/(name+'.tex'); full.write_text(PREAMBLE+fragment+'\n\\end{document}\n',encoding='utf-8')
        result=compile_source(full,build/(name+'-compile'))
        if result['status']!='passed' or result['warnings']: raise RuntimeError(result)
        rendered_result=render(Path(result['pdf']),build/(name+'-render'),220)
        if rendered_result['status']!='rendered' or len(rendered_result['pages'])!=1: raise RuntimeError(rendered_result)
        rendered[name]=crop(Path(rendered_result['pages'][0]))
        evidence.append({'name':name,'source_sha256':sha256(full),'pdf_sha256':sha256(Path(result['pdf'])),'compile':'passed','warnings':result['warnings'],'data':'original synthetic illustration, not experimental measurements'})
    for name in specs: rendered[name].save(images/(name+'.png'))
    width=max(rendered['refinement-before'].width,rendered['benchmark'].width)
    height=rendered['refinement-before'].height+rendered['benchmark'].height+150
    comparison=Image.new('RGB',(width+40,height),'white'); draw=ImageDraw.Draw(comparison)
    y=10
    for label,name in [('Original ruled layout','refinement-before'),('Refined booktabs layout - identical data','benchmark')]:
        draw.text((24,y),label,font=font(25),fill='#243047'); y+=40
        im=rendered[name]; comparison.paste(im,((comparison.width-im.width)//2,y)); y+=im.height+25
    comparison.save(images/'refinement.png')
    write_json(build/'preview-evidence.json',{'figures':evidence,'refinement_body_rows_preserved':len(rows),'all_data_synthetic':True,'visual_review':'pending','images':[{'path':x.name,'sha256':sha256(x)} for x in sorted(images.glob('*.png'))]})
    print('Compiled 3 previews; wrote benchmark.png, ablation.png and refinement.png')

if __name__=='__main__': main()
