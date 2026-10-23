"""Generate editable TeX from a manually reviewed image transcription ledger.

This is not OCR. Ambiguous/illegible cells are shown as [?], never guessed.
Requires only Python's standard library. All cell strings are escaped as text.
"""
import argparse
import hashlib
import json
from pathlib import Path


def escape(text):
    mapping = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(mapping.get(c, c) for c in text)


def styled(text, record):
    for key, macro in [('italic', 'textit'), ('bold', 'textbf'), ('underline', 'underline')]:
        if key in record and not isinstance(record[key], bool): raise ValueError('Style flags must be boolean')
        if record.get(key): text = '\\' + macro + '{' + text + '}'
    return text


def generate(ledger: dict) -> tuple[str, list]:
    columns = ledger['columns']; rows = ledger['rows']
    ids = [c['id'] for c in columns]
    if not ids or len(set(ids)) != len(ids): raise ValueError('Column IDs must be unique')
    row_ids = [r['id'] for r in rows]
    if len(set(row_ids)) != len(row_ids): raise ValueError('Row IDs must be unique')
    unresolved = []
    lines = [r'\begin{table*}[t]', r'\centering', r'\small', r'\setlength{\tabcolsep}{3pt}',
             r'\begin{adjustbox}{max width=\textwidth}',
             r'\begin{tabular}{l' + 'c' * (len(ids) - 1) + '}', r'\toprule']
    groups = ledger.get('header_groups', [])
    if groups:
        if any(not isinstance(g['span'], int) or isinstance(g['span'], bool) or g['span'] < 1 for g in groups) or sum(g['span'] for g in groups) != len(ids):
            raise ValueError('Header groups must cover the columns')
        lines.append(' & '.join(r'\multicolumn{%d}{c}{%s}' % (g['span'], escape(g['label'])) for g in groups) + r' \\')
    lines += [' & '.join((r'\rotatebox{90}{' + styled(escape(c['label']), c) + '}') if c.get('rotate') else styled(escape(c['label']), c) for c in columns) + r' \\', r'\midrule']
    symbols = {'full': r'$\bullet$', 'empty': r'$\circ$'}
    # Half coverage uses a native vector glyph from the TeX symbol font.
    symbols['half'] = r'\raisebox{.1ex}{\tikz{\fill (0,.5ex) arc(90:270:.5ex)--cycle;\draw (0,0) circle(.5ex);}}'
    for row in rows:
        if set(row['cells']) != set(ids): raise ValueError('Each row must contain exactly the declared columns')
        cells = []
        if row.get('rule_before'): lines.append(r'\midrule')
        for col in ids:
            cell = row['cells'][col]; status = cell['status']
            if status not in ('read', 'ambiguous', 'illegible'): raise ValueError('Invalid transcription status')
            if status == 'read' and (('text' in cell) == ('symbol' in cell)):
                raise ValueError('A read cell must contain exactly one of text or symbol')
            if status != 'read':
                unresolved.append({'row': row['id'], 'column': col, 'status': status, 'alternatives': cell.get('alternatives', [])})
                cells.append(r'\textbf{[?]}')
            elif 'symbol' in cell:
                if cell['symbol'] not in symbols: raise ValueError('Unknown coverage symbol')
                cells.append(symbols[cell['symbol']])
            else:
                if not isinstance(cell['text'], str): raise ValueError('Cell text must preserve a string')
                cells.append(styled(escape(cell['text']), cell))
        lines.append(' & '.join(cells) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\end{adjustbox}',
              r'\caption{' + escape(ledger.get('caption', 'Image transcription; unresolved cells are marked [?].')) + '}', r'\end{table*}']
    return '\n'.join(lines) + '\n', unresolved


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('ledger', type=Path); p.add_argument('output', type=Path)
    a = p.parse_args()
    sidecar = a.output.with_suffix('.transcription.json')
    if a.output.exists() or sidecar.exists(): raise ValueError('Use new output paths')
    data = json.loads(a.ledger.read_text(encoding='utf-8-sig'))
    image = (a.ledger.parent / data['image']).resolve()
    digest = hashlib.sha256(image.read_bytes()).hexdigest()
    if digest != data['image_sha256']: raise ValueError('Transcribed image hash mismatch')
    tex, unresolved = generate(data)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(tex, encoding='utf-8')
    sidecar.write_text(json.dumps({'image_sha256': digest,
        'ledger_sha256': hashlib.sha256(a.ledger.read_bytes()).hexdigest(),
        'tex_sha256': hashlib.sha256(a.output.read_bytes()).hexdigest(),
        'unresolved': unresolved, 'transcription': 'manual; not independently verified',
        'numerical_integrity': 'not established by image transcription'}, indent=2), encoding='utf-8')
    print(json.dumps({'status': 'generated', 'unresolved_cells': len(unresolved)}))


if __name__ == '__main__': main()
