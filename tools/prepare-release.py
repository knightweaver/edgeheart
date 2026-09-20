#!/usr/bin/env python3
"""Prepare and harden an Edgeheart GitHub release.

Publication is allowed only when the newly rebuilt runtime archive is
byte-for-byte identical to the Step 8 manually qualified candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--control", type=Path, required=True)
    args = ap.parse_args()

    repo = args.repo.resolve()
    control_path = (repo / args.control).resolve() if not args.control.is_absolute() else args.control.resolve()
    control = json.loads(control_path.read_text(encoding="utf-8"))
    module = json.loads((repo / "module.json").read_text(encoding="utf-8"))
    step8 = json.loads((repo / "build/step8/step8-summary.json").read_text(encoding="utf-8"))
    runtime = json.loads((repo / "build/step7/runtime-package.json").read_text(encoding="utf-8"))

    version = control.get("version")
    tag = control.get("tag")
    if control.get("publish") is not True:
        raise ValueError("Release control must explicitly set publish=true")
    if version != module.get("version"):
        raise ValueError(f"Release version {version} != module.json version {module.get('version')}")
    if tag != f"v{version}":
        raise ValueError(f"Release tag must be v{version}, got {tag}")
    if step8.get("status") != "PASS" or step8.get("releaseGateCleared") is not True:
        raise ValueError("Step 8 runtime qualification PASS is required")
    if runtime.get("status") != "PASS":
        raise ValueError("Current Step 7 runtime-package build is not PASS")

    expected_hash = step8["qualifiedRuntimeCandidate"]["sha256"]
    control_hash = control.get("qualifiedRuntimeSha256")
    current_hash = runtime.get("archiveSha256")
    if control_hash != expected_hash:
        raise ValueError("Release-control qualified hash differs from Step 8")
    if current_hash != expected_hash:
        raise ValueError(
            "Rebuilt runtime archive differs from the manually qualified Step 8 candidate: "
            f"expected {expected_hash}, got {current_hash}"
        )

    archive_name = f"edgeheart-v{version}.zip"
    archive = repo / "release" / archive_name
    if not archive.is_file():
        raise ValueError(f"Runtime archive missing: {archive}")
    actual_hash = sha256(archive)
    if actual_hash != expected_hash:
        raise ValueError(
            f"Runtime archive byte hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    manifest_url = module.get("manifest")
    download_url = module.get("download")
    expected_manifest = "https://github.com/knightweaver/edgeheart/releases/latest/download/module.json"
    expected_download = f"https://github.com/knightweaver/edgeheart/releases/download/{tag}/{archive_name}"
    if manifest_url != expected_manifest:
        raise ValueError(f"module.json manifest URL mismatch: {manifest_url}")
    if download_url != expected_download:
        raise ValueError(f"module.json download URL mismatch: {download_url}")

    release_dir = repo / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    release_module = release_dir / "module.json"
    shutil.copy2(repo / "module.json", release_module)

    checksums = {
        archive_name: sha256(archive),
        "module.json": sha256(release_module),
    }
    checksum_file = release_dir / "SHA256SUMS.txt"
    checksum_file.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
        encoding="utf-8",
    )

    step9_dir = repo / "build/step9"
    step9_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "step": 9,
        "status": "READY_TO_PUBLISH",
        "version": version,
        "tag": tag,
        "qualifiedRuntimeSha256": expected_hash,
        "rebuiltRuntimeSha256": current_hash,
        "byteIdenticalToQualifiedRuntime": True,
        "releaseAssets": [archive_name, "module.json", "SHA256SUMS.txt"],
        "manifestUrl": expected_manifest,
        "downloadUrl": expected_download,
    }
    (step9_dir / "step9-prepublish.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
