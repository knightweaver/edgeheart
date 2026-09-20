#!/usr/bin/env python3
"""Regression tests for Edgeheart maintenance change-impact policy."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path.cwd()

def classify(paths,actor=""):
 cmd=[sys.executable,"tools/maintenance-status.py","--repo",".","--paths",*paths]
 if actor: cmd += ["--actor",actor]
 p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
 try: data=json.loads(p.stdout)
 except Exception as exc: raise AssertionError(f"invalid classifier JSON: {p.stdout}\n{p.stderr}") from exc
 return p.returncode,data

cases=[
 (["README.md"],"",0,"none","none"),
 (["assets/icons/weapons/example.webp"],"",0,"patch","targeted-smoke"),
 (["scripts/competencies.js"],"",0,"patch","full-clean-world"),
 (["sources/edgeheart-consolidated-production-v1.1.zip"],"",0,"minor","full-clean-world"),
 (["module.json"],"",0,"major","full-clean-world"),
]
for paths,actor,code,bump,runtime in cases:
 rc,data=classify(paths,actor)
 assert rc==code,(paths,rc,data)
 assert data["minimumVersionBump"]==bump,(paths,data)
 assert data["runtimeQualification"]==runtime,(paths,data)

rc,data=classify(["src/packs/items/weapons/example.json"])
assert rc==1 and data["status"]=="BLOCK" and data["blockingReasons"],data

rc,data=classify(["src/packs/items/weapons/example.json","tools/build-source-packs.py"])
assert rc==0 and data["status"]=="PASS",data

rc,data=classify(["src/packs/items/weapons/example.json"],"github-actions[bot]")
assert rc==0 and data["status"]=="PASS" and data["warnings"],data

print("Edgeheart maintenance policy regression PASS")
print(" - documentation: no runtime gate")
print(" - asset: patch / targeted smoke")
print(" - runtime code: patch / full clean world")
print(" - canonical source: minor / full clean world")
print(" - module contract: major / full clean world")
print(" - manual direct src/packs edit: BLOCK")
print(" - generated/authorized src/packs edit: PASS")
