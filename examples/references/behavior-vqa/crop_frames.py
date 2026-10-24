#!/usr/bin/env python3
"""Extract the five source photos and write their provenance manifest."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from PIL import Image

CROPS = [
    (91, 95, 234, 237),
    (239, 95, 381, 237),
    (387, 95, 530, 237),
    (535, 95, 678, 237),
    (684, 95, 826, 237),
]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    assets = args.output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    records = []

    with Image.open(args.source) as source:
        if source.size != (915, 713):
            parser.error(f"expected source dimensions 915x713, got {source.width}x{source.height}")
        for index, box in enumerate(CROPS, start=1):
            name = f"frame-{index:02d}.png"
            destination = assets / name
            temporary = assets / f".{name}.tmp"
            source.crop(box).save(temporary, format="PNG")
            os.replace(temporary, destination)
            records.append({
                "file": f"assets/{name}",
                "crop_xyxy_exclusive": list(box),
                "dimensions_px": [box[2] - box[0], box[3] - box[1]],
                "sha256": sha256(destination),
            })

    manifest = {
        "source_file": args.source.name,
        "source_sha256": sha256(args.source),
        "source_size_bytes": args.source.stat().st_size,
        "source_dimensions_px": [915, 713],
        "original_source_tex": "missing",
        "crops": records,
    }
    manifest_path = args.output / "manifest.json"
    temporary_manifest = args.output / ".manifest.json.tmp"
    temporary_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary_manifest, manifest_path)


if __name__ == "__main__":
    main()
