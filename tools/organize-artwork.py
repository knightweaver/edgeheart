#!/usr/bin/env python3
"""Organize Edgeheart artwork using the authoritative Step 6 asset manifest.

This is useful when generated art lives in one flat folder. The output mirrors
Edgeheart/Cybermancy module asset structure. Copy is the default; use --move only
when destructive reorganization is explicitly desired.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

EXPECTED_ASSET_COUNT = 582

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])
    if manifest.get("expectedAssetCount") != EXPECTED_ASSET_COUNT:
        raise ValueError(f"Expected Step 6 asset count {EXPECTED_ASSET_COUNT}")
    if len(entries) != EXPECTED_ASSET_COUNT:
        raise ValueError(f"Manifest contains {len(entries)} entries, expected {EXPECTED_ASSET_COUNT}")
    return manifest

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("destination", type=Path)
    ap.add_argument("--manifest", type=Path, default=Path("build/step6/asset-manifest.json"))
    ap.add_argument("--move", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--allow-missing", action="store_true")
    args = ap.parse_args()

    source = args.source.resolve()
    destination = args.destination.resolve()
    manifest_path = args.manifest.resolve()

    if not source.is_dir():
        raise ValueError(f"Source folder not found: {source}")
    manifest = load_manifest(manifest_path)

    index = defaultdict(list)
    for path in source.rglob("*"):
        if path.is_file():
            index[path.name].append(path)

    missing = []
    ambiguous = []
    planned = []
    for entry in manifest["entries"]:
        matches = index.get(entry["sourceFilename"], [])
        if not matches:
            missing.append(entry["sourceFilename"])
        elif len(matches) > 1:
            ambiguous.append((entry["sourceFilename"], matches))
        else:
            planned.append((matches[0], destination / entry["repositoryPath"]))

    if ambiguous:
        for name, matches in ambiguous[:20]:
            print(f"AMBIGUOUS {name}: {matches}", file=sys.stderr)
        return 2
    if missing and not args.allow_missing:
        print(f"Missing {len(missing)} expected asset(s).", file=sys.stderr)
        for name in missing[:40]:
            print(f" - {name}", file=sys.stderr)
        return 2

    copied = moved = skipped = overwritten = 0
    for src, dst in planned:
        if dst.exists():
            if sha256(src) == sha256(dst):
                skipped += 1
                continue
            if not args.overwrite:
                raise FileExistsError(f"Destination differs: {dst}")
            overwritten += 1

        if args.dry_run:
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        if args.move:
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            moved += 1
        else:
            shutil.copy2(src, dst)
            copied += 1

    print(f"Expected: {EXPECTED_ASSET_COUNT}")
    print(f"Matched: {len(planned)}")
    print(f"Missing: {len(missing)}")
    print(f"Copied: {copied}")
    print(f"Moved: {moved}")
    print(f"Skipped identical: {skipped}")
    print(f"Overwritten: {overwritten}")
    print(f"Dry run: {args.dry_run}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
