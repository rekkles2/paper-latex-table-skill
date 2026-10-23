"""Rebuild a trusted local reference without rewriting its original table fragment.

Requires TeX/Poppler; optional preview cropping and comparison require Pillow.
Compiling unknown TeX requires an appropriate OS sandbox.
"""
import argparse
import json
import shutil
from pathlib import Path

from compile_table import compile_source
from inspect_render import render
from tablelib import ROOT, sha256, write_json


def reproduce(case: Path, output: Path, profile_name: str = 'reproduction/profile.json') -> dict:
    case = case.resolve()
    profile_path = (case / profile_name).resolve()
    if not profile_path.is_relative_to(case): raise ValueError('Profile must stay within the case')
    profile_dir = profile_path.parent
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    source = (profile_dir / profile['source']).resolve()
    macros = (profile_dir / profile['macros']).resolve()
    if not source.is_relative_to(case) or not macros.is_relative_to(case):
        raise ValueError('Profile inputs must stay within the case')
    if output.exists():
        raise ValueError('Use a fresh output directory')
    meta = json.loads((case / 'case.json').read_text(encoding='utf-8-sig'))
    for item in meta['sources']:
        original = (case / item['path']).resolve()
        if not original.is_relative_to(case) or sha256(original) != item['sha256']:
            raise ValueError('Original case source hash mismatch')
    output = output.resolve()
    output.mkdir(parents=True)
    # Stage only declared assets in the requested output. Ordinary reproduction
    # must not create wrapper files inside an installed stable reference case.
    work = output / 'work'; work.mkdir()
    for name in profile.get('assets', []):
        asset = (profile_dir / name).resolve()
        if not asset.is_relative_to(profile_dir) or not asset.is_file():
            raise ValueError('Declared profile asset is missing or outside its directory')
        target = work / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(asset, target)
    wrapper = work / 'document.tex'
    header = '\\documentclass{article}\n\\usepackage[paperwidth=%smm,paperheight=%smm,margin=10mm]{geometry}\n' % (profile['width_mm'] + 20, profile['height_mm'])
    raw = source.read_text(encoding='utf-8-sig')
    wrapper.write_text(header + macros.read_text(encoding='utf-8') + '\n\\begin{document}\n' + raw + '\n\\end{document}\n', encoding='utf-8')
    result = {'case_id': profile['case_id'], 'source_sha256': sha256(source),
              'macros_sha256': sha256(macros), 'profile_sha256': sha256(profile_path),
              'fragment_preservation': 'selected fragment embedded verbatim; immutable original bytes checked separately',
              'selected_source_is_original': any(i['path'] == source.relative_to(case).as_posix() for i in meta['sources']),
              'original_bytes_verified': True, 'notes': profile['notes'], 'visual_review': 'pending'}
    result['compilation'] = compile_source(wrapper, output / 'build', profile['engine'])
    if result['compilation']['status'] == 'passed':
        result['render'] = render(Path(result['compilation']['pdf']), output / 'render', 180)
        try:
            from PIL import Image, ImageChops, ImageOps, ImageDraw
            pages = result['render'].get('pages', [])
            if len(pages) == 1:
                im = Image.open(pages[0]).convert('RGB')
                box = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
                if box:
                    im = ImageOps.expand(im.crop(box), border=8, fill='white')
                    im.save(output / 'reproduced.png')
                    ref = Image.open(case / 'figure.png').convert('RGB')
                    panels = []
                    for label, pic in [('Original reference', ref), ('Editable TeX reconstruction', im)]:
                        pic = pic.resize((1000, max(1, round(pic.height * 1000 / pic.width))))
                        panel = Image.new('RGB', (1020, pic.height + 40), 'white')
                        ImageDraw.Draw(panel).text((10, 8), label, fill='black')
                        panel.paste(pic, (10, 30)); panels.append(panel)
                    sheet = Image.new('RGB', (2040, max(p.height for p in panels)), 'white')
                    sheet.paste(panels[0], (0, 0)); sheet.paste(panels[1], (1020, 0))
                    sheet.save(output / 'comparison.png')
                    result['comparison'] = 'comparison.png; resized panels are visual aids, not integrity proof'
            else:
                result['comparison'] = 'pending: multi-page render requires page-specific review'
        except ImportError:
            result['comparison'] = 'unavailable: optional Pillow not installed'
    write_json(output / 'reproduction-report.json', result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('case', help='Local case ID or case directory')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--profile', default='reproduction/profile.json', help='Profile path relative to the case')
    a = p.parse_args()
    bundled = ROOT / 'assets/cases/local' / a.case
    case = bundled if bundled.is_dir() else Path(a.case)
    result = reproduce(case, a.output, a.profile)
    print(json.dumps({'case_id': result['case_id'], 'status': result['compilation']['status'], 'visual_review': 'pending'}))
    return 0 if result['compilation']['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
