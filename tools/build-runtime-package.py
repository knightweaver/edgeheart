#!/usr/bin/env python3
"""Build a deterministic Edgeheart Foundry runtime-candidate ZIP.

The archive contains only runtime material:
- module.json
- scripts/
- assets/
- compiled packs/

Editable sources, build tooling, upstream source archives, and node_modules are
not shipped in the runtime candidate.

The ZIP is derivative output and is not canonical.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

EXPECTED_ASSETS = 582
EXPECTED_PACKS = 13
FIXED_DT = (1980, 1, 1, 0, 0, 0)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args()
    repo = args.repo.resolve()

    manifest = json.loads((repo / "module.json").read_text(encoding="utf-8"))
    if manifest.get("id") != "edgeheart":
        raise ValueError("module.json id must be edgeheart")
    version = manifest.get("version")
    if not version:
        raise ValueError("module.json version is required")

    asset_files = sorted(
        p for p in (repo / "assets").rglob("*")
        if p.is_file() and p.name != ".gitkeep"
    )
    if len(asset_files) != EXPECTED_ASSETS:
        raise ValueError(
            f"Expected {EXPECTED_ASSETS} runtime asset files, got {len(asset_files)}"
        )

    pack_dirs = []
    for pack in manifest.get("packs", []):
        rel = pack["path"]
        if not rel.endswith(".db"):
            raise ValueError(f"Pack path does not end .db: {rel}")
        compiled_rel = rel[:-3]
        compiled = repo / compiled_rel
        if not compiled.is_dir():
            raise ValueError(f"Compiled pack missing: {compiled_rel}")
        pack_dirs.append(compiled)

    if len(pack_dirs) != EXPECTED_PACKS:
        raise ValueError(f"Expected {EXPECTED_PACKS} compiled packs")

    runtime_files = [repo / "module.json"]
    runtime_files += sorted(p for p in (repo / "scripts").rglob("*") if p.is_file())
    runtime_files += asset_files
    for directory in sorted(pack_dirs):
        runtime_files += sorted(p for p in directory.rglob("*") if p.is_file())

    # Exclude directory-keeping placeholders from releases.
    runtime_files = [p for p in runtime_files if p.name != ".gitkeep"]

    release_dir = repo / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    archive = release_dir / f"edgeheart-v{version}.zip"

    with zipfile.ZipFile(
        archive,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zf:
        for file_path in sorted(runtime_files, key=lambda p: p.relative_to(repo).as_posix()):
            rel = file_path.relative_to(repo).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, file_path.read_bytes())

    digest = sha256(archive)

    report_dir = repo / "build" / "step7"
    report_dir.mkdir(parents=True, exist_ok=True)
    release_manifest = {
        "step": 7,
        "status": "PASS",
        "moduleId": "edgeheart",
        "moduleVersion": version,
        "archive": archive.name,
        "archiveSha256": digest,
        "runtimeFileCount": len(runtime_files),
        "assetFileCount": len(asset_files),
        "compiledCompendiumCount": len(pack_dirs),
        "canonical": False,
        "purpose": "clean-world Foundry runtime qualification candidate",
    }
    (report_dir / "runtime-package.json").write_text(
        json.dumps(release_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(release_manifest, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
