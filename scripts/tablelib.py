"""Small, explicit table contracts. Never a general TeX interpreter."""
from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

def read_json(path: Path) -> Any:
    def unique_object(pairs: list[tuple[str,Any]]) -> dict:
        result={}
        for key,value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key]=value
        return result
    def reject_constant(value: str) -> Any:
        raise ValueError(f'Nonstandard JSON constant: {value}')
    return json.loads(path.read_text(encoding='utf-8-sig'),object_pairs_hook=unique_object,parse_constant=reject_constant)

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def decimal(value: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', value):
        raise ValueError(f'Expected a finite numeric string, got {value!r}')
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError('Nonfinite number')
    return result

def escape(value: str) -> str:
    mapping = {'\\': r'\textbackslash{}', '&':r'\&', '%':r'\%', '$':r'\$', '#':r'\#', '_':r'\_', '{':r'\{', '}':r'\}', '~':r'\textasciitilde{}', '^':r'\textasciicircum{}','<':r'\textless{}','>':r'\textgreater{}'}
    return ''.join(mapping.get(c,c) for c in str(value))

def check_spec(spec: dict) -> None:
    if spec.get('schema_version') != 1:
        raise ValueError('schema_version must be 1')
    columns, rows = spec['columns'], spec['rows']
    if not columns or not rows:
        raise ValueError('Nonempty columns and rows required')
    for items, key in ((columns,'id'), (rows,'id')):
        ids = [x[key] for x in items]
        if any(not isinstance(x,str) or not x for x in ids) or len(set(ids)) != len(ids):
            raise ValueError('IDs must be nonempty unique strings')
    expected = {c['id'] for c in columns}
    for c in columns:
        if c.get('direction') not in ('higher','lower','none'):
            raise ValueError('Every column needs explicit higher/lower/none direction')
        if c.get('kind','number') not in ('number','text'):
            raise ValueError('kind must be number or text')
        if c.get('kind') == 'text' and c['direction'] != 'none':
            raise ValueError('Text cannot be ranked')
    for row in rows:
        if not isinstance(row.get('group','all'),str) or not isinstance(row.get('eligible',True),bool):
            raise ValueError('group must be string; eligible must be bool')
        if set(row['values']) != expected:
            raise ValueError(f"Row {row['id']} has missing/extra columns")
        for c in columns:
            value = row['values'][c['id']]
            if value is None:
                continue
            if c.get('kind','number') == 'text':
                if not isinstance(value,str):
                    raise ValueError('Text must be string')
            elif isinstance(value,dict):
                if set(value) not in ({'mean','std'}, {'mean','ci'}):
                    raise ValueError('Use mean/std or mean/ci explicitly')
                mean = decimal(value['mean'])
                if 'std' in value and decimal(value['std']) < 0:
                    raise ValueError('Negative uncertainty')
                if 'ci' in value:
                    ci = value['ci']
                    if not isinstance(ci,list) or len(ci)!=2 or not decimal(ci[0]) <= mean <= decimal(ci[1]):
                        raise ValueError('CI must contain mean')
                if c['direction'] != 'none' and c.get('rank_on') != 'mean':
                    raise ValueError('Ranking uncertainty needs rank_on=mean; not significance')
            else:
                decimal(value)
    if spec.get('float','table') not in ('table','table*'):
        raise ValueError('float must be table or table*')
    if spec.get('alignment','center') not in ('center','decimal'):
        raise ValueError('alignment must be center or decimal')
    label = spec.get('label','tab:results')
    if not re.fullmatch(r'[A-Za-z0-9:_.-]+',label):
        raise ValueError('Invalid label')
    # Header groups must be contiguous to have a meaningful cmidrule.
    seen, last = set(), None
    for c in columns:
        group = c.get('header_group','')
        if group != last:
            if group and group in seen:
                raise ValueError('header_group must be contiguous')
            seen.add(group)
            last=group

def score(value: Any) -> Decimal:
    return decimal(value['mean'] if isinstance(value,dict) else value)

def rankings(spec: dict) -> dict[tuple[str,str],str]:
    check_spec(spec)
    marks = {}
    for col in spec['columns']:
        if col['direction'] == 'none':
            continue
        for group in {r.get('group','all') for r in spec['rows']}:
            candidates = [r for r in spec['rows'] if r.get('group','all')==group and r.get('eligible',True) and r['values'][col['id']] is not None]
            distinct = sorted({score(r['values'][col['id']]) for r in candidates}, reverse=col['direction']=='higher')
            for row in candidates:
                index = distinct.index(score(row['values'][col['id']]))
                if index < 2:
                    marks[row['id'],col['id']] = ('best','second')[index]
    return marks

def ledger(spec: dict) -> dict:
    """Include identity, grouping, eligibility, units, direction and exact source lexemes."""
    check_spec(spec)
    return {'schema_version':1, 'columns':spec['columns'], 'rows':spec['rows'], **{key:spec[key] for key in ('caption','row_header','label','float','alignment') if key in spec}}

def compare(before: dict, after: dict, *, include_presentation: bool=False) -> list[str]:
    """Keyed data and caption semantics; optionally also protect layout/labels."""
    def keyed(obj):
        return {'columns':{x['id']:x for x in obj['columns']}, 'rows':{x['id']:x for x in obj['rows']}}
    check_spec(before)
    check_spec(after)
    a,b=keyed(before),keyed(after)
    errors=[]
    for kind in ('columns','rows'):
        for key in sorted(set(a[kind]) | set(b[kind])):
            if a[kind].get(key) != b[kind].get(key):
                errors.append(f'{kind}.{key}: changed or missing')
    defaults={'caption':'Results.','row_header':'Method'}
    if include_presentation:
        defaults.update(label='tab:results',float='table',alignment='center')
    for key,default in defaults.items():
        if before.get(key,default)!=after.get(key,default):
            errors.append(f'spec.{key}: changed')
    return errors

def delta(new: str, baseline: str, mode: str) -> Decimal:
    n,b = decimal(new),decimal(baseline)
    with localcontext() as ctx:
        ctx.prec=max(50,len(n.as_tuple().digits)+len(b.as_tuple().digits)+abs(n.adjusted()-b.adjusted())+10)
        if mode in ('absolute','percentage_points'):
            return n-b
        if mode == 'relative_percent':
            if b == 0:
                raise ValueError('Relative change undefined at zero baseline')
            return (n-b)/b*100
    raise ValueError('Unknown delta mode')

def display(value: Any, col: dict) -> str:
    if value is None:
        return '--'
    if col.get('kind') == 'text':
        return escape(value)
    if isinstance(value,dict):
        if 'std' in value:
            return escape(value['mean']) + r'\,$\pm$\,' + escape(value['std'])
        return escape(value['mean']) + ' [' + escape(value['ci'][0]) + ', ' + escape(value['ci'][1]) + ']'
    # Render scientific notation while preserving its original coefficient/exponent digits.
    if 'e' in value.lower():
        coefficient,exponent=re.split('[eE]',value)
        return '$'+coefficient+r'\times 10^{'+exponent+'}$'
    return escape(value)

def generate(spec: dict) -> str:
    check_spec(spec)
    marks = rankings(spec)
    cols=spec['columns']
    use_s = spec.get('alignment')=='decimal'
    if use_s and any(c.get('kind')=='text' or isinstance(r['values'][c['id']],dict) for c in cols for r in spec['rows']):
        raise ValueError('Decimal mode currently supports scalar numeric columns only; use centered rich cells')
    preamble='@{}l' + ''.join('S' if use_s else 'c' for c in cols) + '@{}'
    env=spec.get('float','table')
    lines=[f'% Generated from an explicit data contract. Source precision preserved.', r'% Packages: booktabs' + (', siunitx' if use_s else ''), f'\\begin{{{env}}}[t]', r'\centering', '\\caption{'+escape(spec.get('caption','Results.'))+'}', '\\label{'+spec.get('label','tab:results')+'}', r'\begin{tabular}{'+preamble+'}', r'\toprule']
    if any(c.get('header_group') for c in cols):
        groups=[]
        for i,c in enumerate(cols):
            g=c.get('header_group','')
            if groups and groups[-1][0]==g:
                groups[-1][2]+=1
            else:
                groups.append([g,i+2,1])
        lines.append(' & '+' & '.join('\\multicolumn{'+str(n)+'}{c}{'+escape(g)+'}' for g,start,n in groups)+r' \\')
        lines.append(' '.join('\\cmidrule(lr){'+str(start)+'-'+str(start+n-1)+'}' for g,start,n in groups if g))
    headers=[]
    for c in cols:
        label=c.get('label',c['id']) + (' ('+c['unit']+')' if c.get('unit') else '')
        if c['direction'] != 'none':
            label=escape(label)+(' $\\uparrow$' if c['direction']=='higher' else ' $\\downarrow$')
        else:
            label=escape(label)
        headers.append('{'+label+'}' if use_s else label)
    lines.extend([escape(spec.get('row_header','Method'))+' & '+' & '.join(headers)+r' \\',r'\midrule'])
    current=None
    for row in spec['rows']:
        group=row.get('group','all')
        if current is not None and group != current:
            lines.append(r'\midrule')
        if group != current and group != 'all':
            lines.append('\\multicolumn{'+str(len(cols)+1)+'}{l}{\\textit{'+escape(group)+'}}'+r' \\')
        current=group
        cells=[]
        for col in cols:
            value=row['values'][col['id']]
            text=display(value,col)
            mark=marks.get((row['id'],col['id']))
            if use_s and value is not None and not mark:
                text=value  # S parses the original numeric token, not math-mode TeX.
            if mark:
                text=('\\textbf{' if mark=='best' else '\\underline{')+text+'}'
            if use_s and (mark or value is None):
                # Rich formatting deliberately bypasses S parsing for this cell.
                text=r'\multicolumn{1}{c}{'+text+'}'
            cells.append(text)
        lines.append(escape(row.get('label',row['id']))+' & '+' & '.join(cells)+r' \\')
    lines += [r'\bottomrule',r'\end{tabular}', '\\end{'+env+'}', '']
    return '\n'.join(lines)

def retrieve(cases: list[dict], *, columns: int|None=None, features: list[str]|None=None, table_type: str|None=None, limit: int=5) -> list[dict]:
    required=set(features or [])
    out=[]
    for case in cases:
        observed=set(case.get('features',[]))
        matched=sorted(observed & required)
        s=8*len(matched)-4*len(required-observed)
        if table_type:
            s+=12 if case.get('table_type')==table_type else -4
        if columns is not None:
            n=case.get('columns')
            s += max(-10,6-abs(n-columns)) if isinstance(n,int) else -6
        out.append({'score':s,'matched_features':matched,'case':case})
    return sorted(out,key=lambda x:(-x['score'],x['case']['case_id']))[:limit]

def strip_comments(text: str) -> str:
    lines=[]
    for line in text.splitlines():
        cut=len(line)
        for i,c in enumerate(line):
            if c=='%':
                backslashes=0; j=i-1
                while j>=0 and line[j]=='\\': backslashes+=1; j-=1
                if backslashes%2==0: cut=i; break
        lines.append(line[:cut])
    return '\n'.join(lines)

def static_check(text: str) -> dict:
    """Conservative checks: unsupported macro layouts explicitly reduce coverage."""
    s=strip_comments(text)
    errors,warnings,unsupported=[],[],[]
    stack=[]
    for token in re.finditer(r'\\(?:begin|end)\{([^}]+)\}',s):
        env=token.group(1)
        if token.group().startswith(r'\begin'):
            stack.append(env)
        elif not stack or stack.pop()!=env:
            errors.append('Unbalanced environment '+env)
    if stack:
        errors.append('Unclosed environments: '+','.join(stack))
    braces=0
    for m in re.finditer(r'\\[{}%]|[{}]',s):
        if m.group()=='{': braces+=1
        elif m.group()=='}': braces-=1
        if braces<0:
            errors.append('Unexpected closing brace'); break
    if braces:
        errors.append('Unbalanced braces')
    labels=re.findall(r'\\label\{([^}]+)\}',s)
    if len(labels)!=len(set(labels)):
        errors.append('Duplicate label')
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',s)
    if set(refs)-set(labels):
        warnings.append('References may require external document context: '+', '.join(sorted(set(refs)-set(labels))))
    for pattern,message in [(r'\\(?:tiny|scriptsize)\b','Small font: inspect at publication size'),(r'\\(?:resizebox|scalebox)\b','Scaling: measure final font size'),(r'\\vspace\s*\{\s*-','Negative spacing: inspect collisions')]:
        if re.search(pattern,s): warnings.append(message)
    simple=re.sub(r'@\{\}', '',s)
    tables=list(re.finditer(r'\\begin\{tabular\}(?:\[[^]]*\])?\s*\{([^{}]*)\}(.*?)\\end\{tabular\}',simple,re.S))
    if len(tables) != len(re.findall(r'\\begin\{tabular\}',s)) or re.search(r'\\begin\{(?:tabularx|tabular\*)\}',s):
        unsupported.append('Nested/custom/complex preambles need TeX compilation and manual structure review')
    if re.search(r'\\(?:newcommand|providecommand|renewcommand|def)\b',s):
        unsupported.append('Macro definitions: expansion not interpreted')
    for table in tables:
        pre,body=table.group(1),table.group(2)
        if '|' in pre:
            warnings.append('Vertical rules in preamble')
        if not re.fullmatch(r'[lcrS\s|]+',pre):
            unsupported.append('Column-count checking unavailable for '+pre); continue
        count=len(re.findall('[lcrS]',pre))
        for rule in re.finditer(r'\\(?:cmidrule(?:\([^)]*\))?|cline)\{(\d+)-(\d+)\}',body):
            left,right=map(int,rule.groups())
            if not 1<=left<=right<=count:
                errors.append(f'Rule range {left}-{right} outside {count} columns')
        # Remove rule commands; only split separators outside brace groups.
        body=re.sub(r'\\(?:toprule|midrule|bottomrule|hline|addlinespace)\b(?:\[[^]]*\])?', '',body)
        body=re.sub(r'\\(?:cmidrule(?:\([^)]*\))?|cline)\{\d+-\d+\}', '',body)
        for row in split_top(body,r'\\'):
            row=re.sub(r'^\s*\[[^]]*\]', '',row).strip()
            if not row: continue
            if re.search(r'\\(?:rowcolor|noalign|section\w+|blockrow|component\w+)\b',row):
                unsupported.append('Row-generating/style macro requires manual review'); continue
            cells=split_top(row,'&')
            span=0
            for cell in cells:
                m=re.search(r'\\multicolumn\{(\d+)\}',cell)
                n=int(m.group(1)) if m else 1
                if n<1: errors.append('Multicolumn span must be positive')
                span+=n
            if span!=count:
                errors.append(f'Row spans {span} columns; expected {count}: '+row[:90])
    packages=[]
    for token,package in [('toprule','booktabs'),('multirow','multirow'),('makecell','makecell'),('adjustbox','adjustbox'),('rowcolor','xcolor[table]'),('cellcolor','xcolor[table]'),('tabularx','tabularx')]:
        if '\\'+token in s or '{'+token+'}' in s: packages.append(package)
    if any('S' in table.group(1) for table in tables):
        packages.append('siunitx')
    if r'\addlinespace' in s and 'booktabs' not in packages:
        packages.append('booktabs')
    return {'status':'fail' if errors else 'needs_review' if unsupported else 'static_checks_passed', 'errors':errors,'warnings':sorted(set(warnings)), 'unsupported':sorted(set(unsupported)), 'inferred_packages':packages, 'numerical_integrity':'not_checked_without_data_contract', 'visual_quality':'not_checked'}

def split_top(s: str, separator: str) -> list[str]:
    parts=[]; start=0; depth=0; i=0
    while i<len(s):
        if depth==0 and s.startswith(separator,i):
            parts.append(s[start:i]); i+=len(separator); start=i; continue
        if s[i]=='\\':
            m=re.match(r'\\(?:[A-Za-z]+|.)',s[i:])
            i+=len(m.group()) if m else 1; continue
        if s[i]=='{': depth+=1
        elif s[i]=='}': depth-=1
        i+=1
    parts.append(s[start:]); return parts
