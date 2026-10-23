"""Rebuild original README showcase tables. Requires XeLaTeX, Poppler, Pillow.
Usage: python docs/render_showcase.py --build-root .local/showcase-NEW
All data and capability assignments are synthetic; no private reference is copied.
"""
import argparse,json,sys,hashlib
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from compile_table import compile_source
from inspect_render import render
from PIL import Image,ImageChops,ImageOps
P=r'''\documentclass[10pt]{article}
\usepackage[paperwidth=210mm,paperheight=115mm,margin=8mm]{geometry}
\usepackage{fontspec,booktabs,multirow,amssymb}
\usepackage[table]{xcolor}
\usepackage{tikz}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\definecolor{ink}{HTML}{18283B}
\definecolor{teal}{HTML}{167D8D}
\definecolor{violet}{HTML}{6750A4}
\definecolor{wash}{HTML}{F0EDF8}
\definecolor{mist}{HTML}{EAF3F4}
\definecolor{muted}{HTML}{64748B}
\pagestyle{empty}\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.22}\setlength{\tabcolsep}{5.0pt}
\newcommand{\yes}{\textcolor{teal}{$\checkmark$}}
\newcommand{\no}{\textcolor{muted}{--}}
\newcommand{\full}{\tikz[baseline=-.5ex]\fill[teal] (0,0) circle (2pt);}
\newcommand{\emptyc}{\tikz[baseline=-.5ex]\draw[muted] (0,0) circle (2pt);}
\newcommand{\halfc}{\tikz[baseline=-.5ex]{\fill[teal] (0,0)--(0,2pt) arc (90:270:2pt)--cycle;\draw[teal] (0,0) circle (2pt);}}
\newcommand{\unc}[2]{#1\,{\scriptsize\textcolor{muted}{$\pm$#2}}}
\newcommand{\band}[2]{\rowcolor{mist}\multicolumn{#1}{l}{\textbf{\textit{#2}}}\\}
\newcommand{\titleline}[2]{{\sffamily\small\bfseries\color{teal}#1}\par\smallskip{\Large\bfseries\color{ink}#2}\par\medskip}
\begin{document}\color{ink}
'''
END='\n\\end{document}\n'
def row(c):return ' & '.join(c)+r' \\'+'\n'
def rankrows(records,lower=()):
    out=[]
    for name,vals in records:
        cells=[]
        for j,v in enumerate(vals):
            order=sorted({Decimal(r[1][j]) for r in records},reverse=j not in lower)
            cell=v
            if Decimal(v)==order[0]:cell=r'\textbf{'+v+'}'
            elif Decimal(v)==order[1]:cell=r'\underline{'+v+'}'
            cells.append(cell)
        out.append(row([name]+cells))
    return ''.join(out)
def documents():
    groups=[('Frozen representations',[
        ('Frame encoder',['74.2','69.8','67.1','61.4','58.2','52.7','63.9','7.4']),
        ('Clip encoder',['78.6','73.1','71.4','65.2','61.8','55.9','67.7','9.1']),
        ('Temporal pooling',['80.1','75.6','72.3','67.8','64.2','58.1','69.7','8.6'])]),
        ('Memory-augmented models',[
        ('Local memory',['83.4','78.5','76.1','70.2','67.8','62.4','73.1','12.8']),
        ('Hierarchical memory',['84.7','80.2','78.6','72.5','70.1','65.3','75.2','15.6']),
        ('Prototype retrieval',['85.1','79.8','77.9','73.4','69.7','64.8','75.1','11.3']),
        (r'\textcolor{violet}{\textbf{Atlas / compact}}',['85.8','81.4','79.2','74.6','71.8','66.9','76.6','10.2']),
        (r'\textcolor{violet}{\textbf{Atlas / full}}',['87.3','83.0','81.5','77.2','74.1','69.8','78.8','14.1'])])]
    # One shared comparison scope across families, rather than per-band rankings.
    allrows=[r for _,rs in groups for r in rs]
    ranked=rankrows(allrows,lower=(7,)).splitlines(True)
    main=P+r'''\titleline{01 / MAIN RESULTS}{A hierarchy of evidence, at a glance.}
{\small Three synthetic benchmarks, two settings each; accuracy (\%) $\uparrow$ and latency (ms) $\downarrow$.}\par\medskip
\begin{tabular}{@{}l*{8}{r}@{}}\toprule
\multirow{2}{*}{\textbf{Method}} & \multicolumn{2}{c}{\textbf{SceneBench}} & \multicolumn{2}{c}{\textbf{TimeBench}} & \multicolumn{2}{c}{\textbf{RuleBench}} & \multicolumn{2}{c}{\textbf{Summary}}\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(l){8-9}
 & Static & Shift & Short & Long & Seen & Novel & Mean $\uparrow$ & ms $\downarrow$\\\midrule
'''
    k=0
    for title,rs in groups:
        main+=r'\band{9}{'+title+'}\n'
        for n,v in rs:
            if 'Atlas' in n:main+=r'\rowcolor{wash}'+'\n'
            main+=ranked[k];k+=1
        main+=r'\addlinespace[3pt]'+'\n'
    main+=r'''\bottomrule\end{tabular}
\par\medskip{\footnotesize\textbf{Reading guide.} Bold = best; underline = distinct second, across all rows. Mean averages six accuracy columns.\par Latency measures a separate tradeoff; the highest accuracy is not the fastest model. All names and values are illustrative.}
'''+END
    configs=[('Base',[0,0,0],['76.20','72.10','69.40'],['0.31','0.28','0.35']),('Context',[1,0,0],['78.40','74.20','71.60'],['0.27','0.25','0.30']),('Memory',[0,1,0],['79.10','75.80','72.30'],['0.25','0.22','0.29']),('Context + memory',[1,1,0],['81.30','78.10','75.20'],['0.21','0.20','0.24']),('Full model',[1,1,1],['83.60','80.40','78.10'],['0.18','0.17','0.22'])]
    abl=P+r'''\titleline{02 / ABLATION}{Make every component earn its place.}
{\small Component toggles, quiet uncertainty and explicit gains in one compact layout.}\par\medskip
\begin{tabular}{@{}lccc*{3}{r}r@{}}\toprule
\multirow{2}{*}{\textbf{Configuration}} & \multicolumn{3}{c}{\textbf{Components}} & \multicolumn{3}{c}{\textbf{Accuracy (\%) $\uparrow$}} & \multirow{2}{*}{\textbf{$\Delta$ mean}}\\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}
 & C & M & R & SceneBench & TimeBench & RuleBench & \\\midrule
\band{8}{Compact encoder / mean $\pm$ standard deviation}
'''
    base=sum(map(Decimal,configs[0][2]))/3
    for i,(name,tog,means,std) in enumerate(configs):
        if i==4:abl+=r'\rowcolor{wash}'+'\n';name=r'\textbf{\textcolor{violet}{'+name+'}}'
        cells=[r'\unc{'+(r'\textbf{'+v+'}' if i==4 else r'\underline{'+v+'}' if i==3 else v)+'}{'+s+'}' for v,s in zip(means,std)]
        gain=(sum(map(Decimal,means))/3-base).quantize(Decimal('.01'))
        abl+=row([name]+[r'\yes' if x else r'\no' for x in tog]+cells+([r'\textcolor{teal}{+'+str(gain)+'}'] if i else ['--']))
    abl+=r'''\bottomrule\end{tabular}
\par\medskip{\footnotesize C = context; M = memory; R = rule conditioning. $\Delta$ = mean accuracy change vs. Base, in percentage points.\par Rankings use means only; uncertainty does not imply statistical significance. Synthetic data, not measured experiments.}
'''+END
    rows=[('FrameSet','12k','Image',[2,0,0,0,0,0]),('ClipSet','8k','Clip',[2,2,1,0,0,0]),('EventSet','24k','Clip',[2,2,2,1,0,0]),('StreamSet','6k','Stream',[2,2,2,2,1,0]),('RuleStream','18k','Stream',[2,2,2,2,2,1]),('Atlas suite','32k','Mixed',[2,2,2,2,2,2])]
    matrix=P+r'''\titleline{03 / BENCHMARK MAP}{Show coverage. Expose the gaps.}
{\small A capability matrix with three-state symbols and grouped evaluation axes.}\par\medskip
\begin{tabular}{@{}lllc c c c c c@{}}\toprule
\multirow{2}{*}{\textbf{Collection}} & \multirow{2}{*}{\textbf{Size}} & \multirow{2}{*}{\textbf{Unit}} & \multicolumn{2}{c}{\textbf{Perception}} & \multicolumn{2}{c}{\textbf{Time}} & \multicolumn{2}{c}{\textbf{Definitions}}\\
\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(l){8-9}
 & & & Spatial & Events & Order & Causal & Rules & Updates\\\midrule
'''
    for i,(name,size,unit,cov) in enumerate(rows):
        if i==5:matrix+=r'\rowcolor{wash}'+'\n';name=r'\textbf{\textcolor{violet}{'+name+'}}'
        matrix+=row([name,size,unit]+[{0:r'\emptyc',1:r'\halfc',2:r'\full'}[x] for x in cov])
    matrix+=r'''\bottomrule\end{tabular}
\par\medskip{\footnotesize\full\ full coverage\qquad\halfc\ partial coverage\qquad\emptyc\ not covered\quad(k = thousand units).\par All collections, sizes and coverage assignments are invented to demonstrate layout; they are not a dataset survey.}
'''+END
    return {'showcase-main':main,'showcase-ablation':abl,'showcase-coverage':matrix}, {'main_groups':groups,'ablation':configs,'coverage':rows}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build-root',required=True,type=Path);a=ap.parse_args()
    a.build_root.mkdir(parents=True,exist_ok=False)
    docs,data=documents(); dest=ROOT/'docs/examples/showcase';dest.mkdir(exist_ok=True)
    (dest/'data.json').write_text(json.dumps({'synthetic':True,'data':data},indent=2)+'\n',encoding='utf8')
    evidence=[]
    for name,tex in docs.items():
        source=dest/(name+'.tex');source.write_text(tex,encoding='utf8')
        result=compile_source(source,a.build_root/(name+'-compile'),engine='xelatex')
        if result['status']!='passed' or result['warnings']:raise RuntimeError({k:v for k,v in result.items() if k!='runs'})
        rendered=render(Path(result['pdf']),a.build_root/(name+'-render'),240)
        if rendered['status']!='rendered' or len(rendered['pages'])!=1:raise RuntimeError(rendered)
        im=Image.open(rendered['pages'][0]).convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda x:255 if x>18 else 0).getbbox()
        im=ImageOps.expand(im.crop(box),border=32,fill='white');out=ROOT/'docs/images'/(name+'.png');im.save(out)
        evidence.append({'name':name,'compile':result['status'],'warnings':result['warnings'],'engine':result['engine'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'visual_review':'pending'})
        print(name+': compiled and rendered',flush=True)
    (a.build_root/'evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
if __name__=='__main__':main()
