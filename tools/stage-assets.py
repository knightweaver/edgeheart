#!/usr/bin/env python3
"""Stage Edgeheart artwork into the module asset tree.

The source directory may be flat or nested. Filenames must match
build/step6/asset-manifest.json exactly.

The Step 6 dual-art contract contains 582 required assets:
- 538 source-document primary WebP images
- 11 Competency illustration WebPs
- 11 Competency UI-glyph SVGs
- 22 adversary token PNGs
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

EXPECTED_ASSET_COUNT = 582

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("generated_art", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Stage the available subset without failing for missing expected files."
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    source = args.generated_art.resolve()
    manifest_path = repo / "build/step6/asset-manifest.json"

    if not source.is_dir():
        raise ValueError(f"Generated-art directory not found: {source}")
    if not manifest_path.is_file():
        raise ValueError(
            "build/step6/asset-manifest.json is missing; run "
            "python tools/rewrite-asset-paths.py first"
        )

    manifest = load_json(manifest_path)
    entries = manifest.get("entries", [])
    if manifest.get("expectedAssetCount") != EXPECTED_ASSET_COUNT or len(entries) != EXPECTED_ASSET_COUNT:
        raise ValueError(f"Expected a {EXPECTED_ASSET_COUNT}-entry Step 6 asset manifest")

    found = defaultdict(list)
    for path in source.rglob("*"):
        if path.is_file():
            found[path.name].append(path)

    staged = 0
    missing = []
    duplicates = []
    for entry in entries:
        filename = entry["sourceFilename"]
        matches = found.get(filename, [])
        if not matches:
            missing.append(filename)
            continue
        if len(matches) > 1:
            duplicates.append({
                "filename": filename,
                "matches": [str(p) for p in matches],
            })
            continue

        destination = repo / entry["repositoryPath"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(matches[0], destination)
        staged += 1

    if duplicates:
        print("Duplicate filenames prevent deterministic staging:", file=sys.stderr)
        for item in duplicates[:20]:
            print(f" - {item['filename']}: {item['matches']}", file=sys.stderr)
        return 1

    if missing and not args.allow_missing:
        print(
            f"Staged {staged} assets but {len(missing)} expected files were missing.",
            file=sys.stderr,
        )
        print("First missing files:", file=sys.stderr)
        for name in missing[:30]:
            print(f" - {name}", file=sys.stderr)
        return 1

    print(f"Edgeheart asset staging complete: {staged} file(s) copied")
    print(f"Missing expected files: {len(missing)}")
    if missing and args.allow_missing:
        print("Partial staging accepted because --allow-missing was supplied.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
