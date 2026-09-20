#!/usr/bin/env python3
"""Compare a rebuilt runtime package to the manually qualified Step 8 package.

Foundry's LevelDB compiler writes per-pack LOG and LOG.old files containing
ephemeral LevelDB logging metadata. Those files are not stable byte-for-byte
across otherwise identical compilations.

For release hardening, every ZIP member must exist in both packages and every
member must be byte-identical except exactly those LevelDB LOG/LOG.old files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ALLOWED = re.compile(r"^packs/.+/(LOG|LOG\.old)$")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path.cwd())
    ap.add_argument("--qualified",type=Path,required=True)
    ap.add_argument("--rebuilt",type=Path,required=True)
    args=ap.parse_args()
    repo=args.repo.resolve()
    qualified=args.qualified.resolve()
    rebuilt=args.rebuilt.resolve()

    with zipfile.ZipFile(qualified) as qz, zipfile.ZipFile(rebuilt) as rz:
        qnames=qz.namelist()
        rnames=rz.namelist()
        if qnames != rnames:
            qset=set(qnames); rset=set(rnames)
            raise ValueError(
                "Runtime ZIP member lists differ; "
                f"missing={sorted(qset-rset)[:10]} extra={sorted(rset-qset)[:10]}"
            )

        exact=[]
        allowed=[]
        forbidden=[]
        for name in qnames:
            qbytes=qz.read(name)
            rbytes=rz.read(name)
            if qbytes == rbytes:
                exact.append(name)
                continue
            record={
                "path":name,
                "qualifiedSha256":hashlib.sha256(qbytes).hexdigest(),
                "rebuiltSha256":hashlib.sha256(rbytes).hexdigest(),
                "qualifiedSize":len(qbytes),
                "rebuiltSize":len(rbytes),
            }
            if ALLOWED.match(name):
                allowed.append(record)
            else:
                forbidden.append(record)

    if forbidden:
        raise ValueError(
            "Rebuilt runtime differs from qualified runtime outside permitted "
            f"LevelDB log files: {[x['path'] for x in forbidden[:10]]}"
        )

    expected_allowed=26
    if len(allowed) != expected_allowed:
        raise ValueError(
            f"Expected exactly {expected_allowed} variable LevelDB log files, got {len(allowed)}"
        )

    report={
        "step":9,
        "status":"PASS",
        "comparison":"qualified Step 8 runtime vs fresh rebuilt runtime",
        "qualifiedSha256":sha256(qualified),
        "rebuiltSha256":sha256(rebuilt),
        "zipMemberCount":len(qnames),
        "byteIdenticalMemberCount":len(exact),
        "permittedLevelDbLogDifferenceCount":len(allowed),
        "forbiddenDifferenceCount":0,
        "permittedDifferences":allowed,
        "releasePolicy":{
            "publishExactQualifiedArchive":True,
            "freshRebuildMustMatchAllNonLogMembers":True,
            "levelDbLogFilesAreEphemeral":True
        }
    }
    out=repo/"build/step9/runtime-equivalence.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
