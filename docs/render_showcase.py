"""Compile paper-style README examples; all data are synthetic.
python docs/render_showcase.py --build-root .local/academic-NEW
Requires XeLaTeX, TeX Gyre Termes, Poppler and Pillow.
"""
import argparse,hashlib,json,sys,re
from pathlib import Path
from decimal import Decimal
from PIL import Image,ImageChops,ImageOps
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from compile_table import compile_source
from inspect_render import render
P=r'''\documentclass[10pt]{article}
\usepackage[paperwidth=190mm,paperheight=140mm,margin=7mm]{geometry}
\usepackage{fontspec,booktabs,multirow,amssymb,graphicx}
\usepackage[table]{xcolor}
\usepackage{tikz}
\setmainfont{TeX Gyre Termes}
\definecolor{sectiongray}{gray}{0.91}
\definecolor{selected}{RGB}{237,249,237}
\definecolor{quiet}{gray}{0.42}
\definecolor{gain}{RGB}{0,105,32}
\pagestyle{empty}\setlength{\parindent}{0pt}
\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.04}
\newcommand{\captext}[3]{\noindent Table #1: \textbf{#2} #3\par\vspace{5pt}}
\newcommand{\band}[2]{\rowcolor{sectiongray}\multicolumn{#1}{l}{\textit{#2}}\\}
\newcommand{\unc}[2]{#1\,{\scriptsize\textcolor{quiet}{$\pm$#2}}}
\newcommand{\yes}{$\checkmark$}
\newcommand{\no}{--}
\newcommand{\full}{\tikz[baseline=-.5ex]\fill (0,0) circle (1.8pt);}
\newcommand{\emptyc}{\tikz[baseline=-.5ex]\draw (0,0) circle (1.8pt);}
\newcommand{\halfc}{\tikz[baseline=-.5ex]{\fill (0,0)--(0,1.8pt) arc (90:270:1.8pt)--cycle;\draw (0,0) circle (1.8pt);}}
\begin{document}
'''
END='\n\\end{document}\n'
def row(c):return ' & '.join(c)+r' \\'+'\n'
def clean(n):
    m=re.fullmatch(r'\\textcolor\{violet\}\{\\textbf\{(.+)\}\}',n)
    return m.group(1) if m else n

def rankcell(v,values,lower=False):
    order=sorted(set(map(Decimal,values)),reverse=not lower)
    if Decimal(v)==order[0]:return r'\textbf{'+v+'}'
    if len(order)>1 and Decimal(v)==order[1]:return r'\underline{'+v+'}'
    return v

def documents():
    original=json.loads((ROOT/'docs/examples/showcase/data.json').read_text(encoding='utf8'))['data']
    groups=original['main_groups'];allrows=[r for _,rs in groups for r in rs]
    ledger={'synthetic':True,'source_data':'docs/examples/showcase/data.json','cells':[],'additional':{}}
    main=P+r'''\captext{1}{Multi-benchmark comparison.}{Accuracy (\%) is reported under static and shifted scenes, short and long temporal contexts, and seen and novel rules. Bold and underline mark the best and distinct second-best values across all methods. All data are synthetic.}
\begin{center}\begin{tabular}{@{}l*{8}{r}@{}}\toprule
\multirow{2}{*}{Method} & \multicolumn{2}{c}{SceneBench} & \multicolumn{2}{c}{TimeBench} & \multicolumn{2}{c}{RuleBench} & \multicolumn{2}{c}{Summary}\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(l){8-9}
 & \rotatebox{65}{Static $\uparrow$} & \rotatebox{65}{Shift $\uparrow$} & \rotatebox{65}{Short $\uparrow$} & \rotatebox{65}{Long $\uparrow$} & \rotatebox{65}{Seen $\uparrow$} & \rotatebox{65}{Novel $\uparrow$} & Mean $\uparrow$ & ms $\downarrow$\\\midrule
'''
    for group,rs in groups:
        main+=r'\band{9}{'+group+'}\n'
        for name,vals in rs:
            name=clean(name)
            if name.startswith('Atlas'):main+=r'\rowcolor{selected}'+'\n';label=r'\textbf{'+name+'}'
            else:label=name
            main+=row([label]+[rankcell(v,[r[1][j] for r in allrows],j==7) for j,v in enumerate(vals)])
            ledger['cells'] += [{'table':'main','row':name,'column':j,'source':v,'rendered':v} for j,v in enumerate(vals)]
    main+=r'''\bottomrule\end{tabular}\end{center}
{\footnotesize Mean averages the six accuracy columns. Latency is in milliseconds; lower is better.}
'''+END
    configs=original['ablation'];base=sum(map(Decimal,configs[0][2]))/3
    abl=P+r'''\captext{2}{Component ablation.}{All variants use the same compact encoder. Entries report synthetic mean accuracy (\%) $\pm$ standard deviation; $\Delta$ is the mean change from Base in percentage points.}
\begin{center}\begin{tabular}{@{}lccc*{3}{r}r@{}}\toprule
\multirow{2}{*}{Variant} & \multicolumn{3}{c}{Components} & \multicolumn{3}{c}{Accuracy $\uparrow$} & \multirow{2}{*}{$\Delta$ mean}\\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}
 & C & M & R & SceneBench & TimeBench & RuleBench & \\\midrule
'''
    for i,(name,tog,means,std) in enumerate(configs):
        if i==len(configs)-1:abl+=r'\rowcolor{sectiongray}'+'\n';label=r'\textbf{'+name+'}'
        else:label=name
        vals=[r'\unc{'+rankcell(v,[r[2][j] for r in configs])+'}{'+std[j]+'}' for j,v in enumerate(means)]
        delta=(sum(map(Decimal,means))/3-base).quantize(Decimal('.01'))
        abl+=row([label]+[r'\yes' if x else r'\no' for x in tog]+vals+['--' if i==0 else '+'+str(delta)])
        ledger['cells'] += [{'table':'ablation','row':name,'column':j,'source':v,'rendered':v,'std':std[j]} for j,v in enumerate(means)]
    abl+=r'''\bottomrule\end{tabular}\end{center}
{\footnotesize C: context; M: memory; R: rule conditioning. Ranking uses means, without a significance claim.}
'''+END
    matrix=P+r'''\captext{3}{Coverage of illustrative evaluation collections.}{Perception, temporal reasoning and definition updates are separated to expose differences in evaluation scope. Names, sizes and coverage assignments are synthetic.}
\begin{center}\begin{tabular}{@{}lll*{6}{c}@{}}\toprule
\multirow{2}{*}{Collection} & \multirow{2}{*}{Size} & \multirow{2}{*}{Unit} & \multicolumn{2}{c}{Perception} & \multicolumn{2}{c}{Time} & \multicolumn{2}{c}{Definitions}\\
\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(l){8-9}
 & & & Spatial & Events & Order & Causal & Rules & Updates\\\midrule
'''
    for i,(name,size,unit,cov) in enumerate(original['coverage']):
        if i==5:matrix+=r'\rowcolor{sectiongray}'+'\n';name=r'\textbf{'+name+'}'
        matrix+=row([name,size,unit]+[{0:r'\emptyc',1:r'\halfc',2:r'\full'}[x] for x in cov])
    matrix+=r'''\bottomrule\end{tabular}\end{center}
{\footnotesize\full\ full coverage;\quad\halfc\ partial coverage;\quad\emptyc\ not covered. k denotes thousand units.}
'''+END
    panels=[('Model depth','Blocks',['6','12','18','24'],['78.2','80.4','81.1','81.3'],['8.1','10.2','13.8','17.6'],1),('Memory size','Slots',['16','32','64','128'],['78.9','80.4','81.0','81.2'],['9.3','10.2','12.6','16.1'],1),('Context length','Frames',['8','16','32','64'],['77.1','79.2','80.4','80.9'],['6.8','8.4','10.2','14.8'],2),('Retrieval budget','Top-k',['1','2','4','8'],['78.6','79.7','80.4','80.8'],['8.7','9.2','10.2','12.4'],2)]
    panel=P+r'''\captext{4}{Sensitivity to model and inference settings.}{One factor varies in each panel; all other settings remain at the gray default. Accuracy (\%) and latency (ms) are synthetic. Bold marks the best value within each panel and column.}
\vspace{3pt}
'''
    for i,(title,head,settings,acc,lat,default) in enumerate(panels):
        panel+=r'\begin{minipage}[t]{.24\linewidth}\centering\setlength{\tabcolsep}{3pt}'+'\n'
        panel+=r'\begin{tabular}{@{}rrr@{}}\toprule'+'\n'+row([head,r'Acc.$\uparrow$',r'ms$\downarrow$'])+r'\midrule'+'\n'
        for j,x in enumerate(settings):
            if j==default:panel+=r'\rowcolor{sectiongray}'+'\n'
            panel+=row([x,r'\textbf{'+acc[j]+'}' if Decimal(acc[j])==max(map(Decimal,acc)) else acc[j],r'\textbf{'+lat[j]+'}' if Decimal(lat[j])==min(map(Decimal,lat)) else lat[j]])
        panel+=r'\bottomrule\end{tabular}\par\smallskip\raggedright ('+chr(97+i)+r') \textbf{'+title+r'.}\end{minipage}'+'\n'+(r'\hfill'+'\n' if i<3 else '')
    panel+=END;ledger['additional']['sensitivity']=panels
    paired=P+r'''\captext{5}{Paired comparison with rule conditioning.}{Each pair uses the same encoder and evaluation setting. Parentheses report changes relative to its own baseline. Values are synthetic; accuracy is in \% and latency in ms.}
\begin{center}\begin{tabular}{@{}llrr@{}}\toprule
Encoder & Setting & Accuracy $\uparrow$ & Latency $\downarrow$\\\midrule
'''
    pairs=[('Small',['76.2','8.0'],['79.4','8.6']),('Base',['80.4','10.2'],['83.1','11.0']),('Large',['83.6','14.1'],['85.2','15.3'])]
    for i,(name,a,b) in enumerate(pairs):
        if i:paired+=r'\midrule'+'\n'
        paired+=row([r'\multirow{2}{*}{'+name+'}','baseline']+a)
        delta=[Decimal(b[j])-Decimal(a[j]) for j in range(2)]
        paired+=row(['',r'\textbf{+ rules}',r'\textbf{'+b[0]+r'} {\small\textcolor{gain}{(+'+str(delta[0])+')}}',b[1]+r' {\small (+'+str(delta[1])+')}'])
    paired+=r'''\bottomrule\end{tabular}\end{center}
{\footnotesize Accuracy changes are percentage points. Green indicates higher accuracy; latency increases remain black.}
'''+END;ledger['additional']['paired']=pairs
    return {'showcase-main':main,'showcase-ablation':abl,'showcase-coverage':matrix,'showcase-sensitivity':panel,'showcase-paired':paired},ledger

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build-root',required=True,type=Path);a=ap.parse_args()
    a.build_root.mkdir(parents=True,exist_ok=False)
    docs,ledger=documents();dest=ROOT/'docs/examples/showcase';evidence=[]
    for name,tex in docs.items():
        source=dest/(name+'.tex');source.write_text(tex,encoding='utf8')
        result=compile_source(source,a.build_root/(name+'-compile'),engine='xelatex')
        if result['status']!='passed' or result['warnings']:raise RuntimeError({k:v for k,v in result.items() if k!='runs'})
        rendered=render(Path(result['pdf']),a.build_root/(name+'-render'),240)
        if rendered['status']!='rendered' or len(rendered['pages'])!=1:raise RuntimeError(rendered)
        im=Image.open(rendered['pages'][0]).convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda x:255 if x>18 else 0).getbbox()
        im=ImageOps.expand(im.crop(box),border=16,fill='white');out=ROOT/'docs/images'/(name+'.png');im.save(out)
        evidence.append({'name':name,'compile':result['status'],'warnings':result['warnings'],'engine':result['engine'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'body_pt':10,'scaling':False,'visual_review':'pending'})
        print(name+': compiled and rendered',flush=True)
    (dest/'academic-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf8')
    (a.build_root/'evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
if __name__=='__main__':main()
