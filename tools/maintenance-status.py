#!/usr/bin/env python3
from __future__ import annotations
import argparse, fnmatch, json, subprocess
from pathlib import Path

def load(p:Path): return json.loads(p.read_text(encoding="utf-8"))
def matches(path:str,pattern:str)->bool:
 return fnmatch.fnmatch(path,pattern) or (pattern.endswith("/**") and path.startswith(pattern[:-3]+"/"))
def git_paths(repo:Path,base:str,head:str)->list[str]:
 p=subprocess.run(["git","diff","--name-only",base,head],cwd=repo,check=True,text=True,capture_output=True)
 return [x.strip().replace("\\","/") for x in p.stdout.splitlines() if x.strip()]
def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,default=Path.cwd()); ap.add_argument("--base"); ap.add_argument("--head",default="HEAD"); ap.add_argument("--paths",nargs="*"); ap.add_argument("--output",type=Path); a=ap.parse_args()
 repo=a.repo.resolve(); m=load(repo/"maintenance/change-impact-v1.json")
 if a.paths: paths=[p.replace("\\","/") for p in a.paths]
 elif a.base: paths=git_paths(repo,a.base,a.head)
 else: raise ValueError("Provide --base/--head or explicit --paths")
 impacts=[]; gates=set(); severity="none"; runtime="none"
 for rule in m["rules"]:
  hit=sorted({p for p in paths if any(matches(p,pat) for pat in rule["patterns"])})
  if not hit: continue
  impacts.append({"rule":rule["id"],"paths":hit}); gates.update(rule.get("gates",[]))
  if m["severityOrder"].index(rule["minimumVersionBump"])>m["severityOrder"].index(severity): severity=rule["minimumVersionBump"]
  if m["runtimeOrder"].index(rule["runtimeQualification"])>m["runtimeOrder"].index(runtime): runtime=rule["runtimeQualification"]
 matched={p for i in impacts for p in i["paths"]}; unmatched=sorted(set(paths)-matched)
 derived=[p for p in paths if matches(p,m["derivedSourcePolicy"]["path"])]
 companion=any(matches(p,pat) for p in paths for pat in m["derivedSourcePolicy"]["authorizedCompanionPatterns"])
 blocking=[]
 if derived and not companion: blocking.append("src/packs is generated authority: direct source-pack changes require an accepted source or generator/compatibility change.")
 report={"status":"BLOCK" if blocking else "PASS","changedPaths":sorted(paths),"impacts":impacts,"unmatchedPaths":unmatched,"requiredGates":sorted(gates),"minimumVersionBump":severity,"runtimeQualification":runtime,"blockingReasons":blocking}
 if a.output:
  out=(repo/a.output).resolve() if not a.output.is_absolute() else a.output.resolve(); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,indent=2)); return 1 if blocking else 0
if __name__=="__main__": raise SystemExit(main())
