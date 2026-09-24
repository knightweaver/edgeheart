#!/usr/bin/env python3
"""Prepare a release from the exact manually qualified runtime archive.

A fresh rebuild must pass all deterministic gates and match the qualified
archive except for ephemeral LevelDB LOG/LOG.old files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path.cwd())
    ap.add_argument("--control",type=Path,required=True)
    args=ap.parse_args()
    repo=args.repo.resolve()
    control_path=(repo/args.control).resolve() if not args.control.is_absolute() else args.control.resolve()

    control=json.loads(control_path.read_text(encoding="utf-8"))
    module=json.loads((repo/"module.json").read_text(encoding="utf-8"))
    step8=json.loads((repo/"build/step8/step8-summary.json").read_text(encoding="utf-8"))
    runtime=json.loads((repo/"build/step7/runtime-package.json").read_text(encoding="utf-8"))
    equivalence=json.loads((repo/"build/step9/runtime-equivalence.json").read_text(encoding="utf-8"))

    version=control.get("version")
    tag=control.get("tag")
    if control.get("publish") is not True:
        raise ValueError("Release control must explicitly set publish=true")
    if version != module.get("version"):
        raise ValueError(f"Release version {version} != module.json version {module.get('version')}")
    if tag != f"v{version}":
        raise ValueError(f"Release tag must be v{version}, got {tag}")
    if step8.get("status") != "PASS" or step8.get("releaseGateCleared") is not True:
        raise ValueError("Step 8 runtime qualification PASS is required")
    if version == "0.2.0":
        baseline=json.loads((repo/"maintenance/baseline-v0.2.0.json").read_text(encoding="utf-8"))
        qualification=baseline["qualification"]
        if (qualification.get("status") != "PASS"
                or qualification.get("cleanWorld") != "PASS"
                or qualification.get("legacyWorldUpgrade") != "PASS"):
            raise ValueError("v0.2.0 requires clean-world and copied legacy-world qualification PASS")
        if qualification.get("qualifiedArtifactSha256") != step8["qualifiedRuntimeCandidate"]["sha256"]:
            raise ValueError("v0.2.0 baseline qualified hash differs from Step 8")
        if step8.get("runtime") != {
            "foundryCore": "14.368", "systemId": "daggerheart",
            "systemVersion": "2.10.5", "moduleId": "edgeheart", "moduleVersion": "0.2.0"
        }:
            raise ValueError("v0.2.0 Step 8 runtime does not match the qualification target")
    if runtime.get("status") != "PASS":
        raise ValueError("Fresh Step 7 rebuild is not PASS")
    if equivalence.get("status") != "PASS" or equivalence.get("forbiddenDifferenceCount") != 0:
        raise ValueError("Fresh rebuild did not pass runtime equivalence validation")

    expected_hash=step8["qualifiedRuntimeCandidate"]["sha256"]
    if control.get("qualifiedRuntimeSha256") != expected_hash:
        raise ValueError("Release-control qualified hash differs from Step 8")
    if equivalence.get("qualifiedSha256") != expected_hash:
        raise ValueError("Downloaded qualified artifact hash differs from Step 8")

    rebuilt_hash=runtime.get("archiveSha256")
    if equivalence.get("rebuiltSha256") != rebuilt_hash:
        raise ValueError("Equivalence report rebuilt hash differs from current Step 7 build")

    archive_name=f"edgeheart-v{version}.zip"
    archive=repo/"release"/archive_name
    if not archive.is_file():
        raise ValueError(f"Qualified runtime archive missing: {archive}")
    actual_hash=sha256(archive)
    if actual_hash != expected_hash:
        raise ValueError(
            f"Published archive must be exact Step 8 candidate: expected {expected_hash}, got {actual_hash}"
        )

    expected_manifest="https://github.com/knightweaver/edgeheart/releases/latest/download/module.json"
    expected_download=f"https://github.com/knightweaver/edgeheart/releases/download/{tag}/{archive_name}"
    if module.get("manifest") != expected_manifest:
        raise ValueError(f"module.json manifest URL mismatch: {module.get('manifest')}")
    if module.get("download") != expected_download:
        raise ValueError(f"module.json download URL mismatch: {module.get('download')}")

    release_dir=repo/"release"
    release_module=release_dir/"module.json"
    shutil.copy2(repo/"module.json",release_module)

    checksums={
        archive_name:sha256(archive),
        "module.json":sha256(release_module),
    }
    (release_dir/"SHA256SUMS.txt").write_text(
        "".join(f"{digest}  {name}\n" for name,digest in sorted(checksums.items())),
        encoding="utf-8"
    )

    summary={
        "step":9,
        "status":"READY_TO_PUBLISH",
        "version":version,
        "tag":tag,
        "qualifiedRuntimeSha256":expected_hash,
        "freshRebuildSha256":rebuilt_hash,
        "publishedArchiveIsExactQualifiedRuntime":True,
        "freshRebuildEquivalentExceptLevelDbLogs":True,
        "byteIdenticalZipMembers":equivalence["byteIdenticalMemberCount"],
        "permittedLevelDbLogDifferences":equivalence["permittedLevelDbLogDifferenceCount"],
        "releaseAssets":[archive_name,"module.json","SHA256SUMS.txt"],
        "manifestUrl":expected_manifest,
        "downloadUrl":expected_download,
    }
    step9=repo/"build/step9"
    step9.mkdir(parents=True,exist_ok=True)
    (step9/"step9-prepublish.json").write_text(
        json.dumps(summary,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps(summary,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
