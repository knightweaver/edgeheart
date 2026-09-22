#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from pathlib import Path
from typing import Any

def load(p:Path)->Any: return json.loads(p.read_text(encoding="utf-8"))
def sha256(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def get_path(v:Any,dotted:str)->Any:
 cur=v
 for part in dotted.split("."):
  if part=="length": return len(cur)
  if isinstance(cur,dict) and part in cur: cur=cur[part]
  else: raise KeyError(dotted)
 return cur

def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,default=Path.cwd()); a=ap.parse_args()
 repo=a.repo.resolve(); module=load(repo/"module.json"); baseline_path=repo/f"maintenance/baseline-v{module.get('version')}.json"; b=load(baseline_path); f=load(repo/"maintenance/regression-fixtures-v1.json")
 assets=load(repo/"build/step6/asset-manifest.json"); registry=load(repo/"build/step3/stable-id-registry.json")
 errors=[]
 if module.get("version")!=b["moduleVersion"]: errors.append("module version differs from baseline")
 compat=module.get("compatibility",{})
 expected_foundry=b["declaredCompatibility"]["foundry"]
 if any(compat.get(k)!=expected_foundry.get(k) for k in ("minimum","verified","maximum")): errors.append("Foundry compatibility differs from baseline")
 dh=next((x for x in module.get("relationships",{}).get("systems",[]) if x.get("id")=="daggerheart"),None)
 expected_dh=b["declaredCompatibility"]["daggerheart"]
 if not dh or any(dh.get("compatibility",{}).get(k)!=expected_dh.get(k) for k in ("minimum","verified")) or dh.get("compatibility",{}).get("maximum") is not expected_dh.get("maximum"): errors.append("Daggerheart compatibility differs from baseline")
 arc=repo/b["sourceArchive"]["path"]
 if not arc.is_file(): errors.append("canonical source archive missing")
 elif sha256(arc)!=b["sourceArchive"]["sha256"]: errors.append("canonical source archive SHA-256 differs from baseline")
 docs={}; folders=0; docs_by_pack=Counter(); entries_by_pack=Counter()
 for pack in module.get("packs",[]):
  rel=pack["path"][:-3] if pack["path"].endswith(".db") else pack["path"]; d=repo/"src"/rel
  if not d.is_dir(): errors.append(f"missing source pack directory: {rel}"); continue
  for p in d.glob("*.json"):
   doc=load(p); entries_by_pack[pack["name"]]+=1
   if str(doc.get("_key","")).startswith("!folders!"): folders+=1; continue
   key=doc.get("flags",{}).get("edgeheart",{}).get("deployment",{}).get("logicalKey")
   if not key: errors.append(f"{p.relative_to(repo)} missing logicalKey"); continue
   if key in docs: errors.append(f"duplicate logicalKey: {key}")
   docs[key]=(p,doc); docs_by_pack[pack["name"]]+=1
 if len(docs)!=b["sourceDocuments"]: errors.append(f"source document count {len(docs)} != {b['sourceDocuments']}")
 if folders!=b["structuralFolders"]: errors.append(f"folder count {folders} != {b['structuralFolders']}")
 if sum(entries_by_pack.values())!=b["sourcePackEntries"]: errors.append("source pack entry total differs from baseline")
 for pack,count in b["documentsByPack"].items():
  if docs_by_pack[pack]!=count: errors.append(f"{pack} document count {docs_by_pack[pack]} != {count}")
 for pack,count in b["entriesByPack"].items():
  if entries_by_pack[pack]!=count: errors.append(f"{pack} entry count {entries_by_pack[pack]} != {count}")
 if len(registry.get("documents",{}))!=b["sourceDocuments"]: errors.append("stable ID registry count differs from baseline")
 if assets.get("expectedAssetCount")!=b["assets"]["total"] or len(assets.get("entries",[]))!=b["assets"]["total"]: errors.append("asset manifest total differs from baseline")
 missing=[e["repositoryPath"] for e in assets.get("entries",[]) if not (repo/e["repositoryPath"]).is_file()]
 if missing: errors.append(f"{len(missing)} baseline assets are missing")
 cards=Counter()
 for key,(_,doc) in docs.items():
  if key.startswith("domainCard:"): cards[doc.get("system",{}).get("domain")]+=1
 if sum(cards.values())!=b["competencies"]["totalCards"]: errors.append("Domain Card total differs from baseline")
 for domain in b["competencies"]["ids"]:
  if cards[domain]!=b["competencies"]["cardsPerCompetency"]: errors.append(f"{domain} card count {cards[domain]} differs from baseline")
  for ext in ("webp","svg"):
   if not (repo/f"assets/icons/domains/{domain}.{ext}").is_file(): errors.append(f"missing Competency asset {domain}.{ext}")
 for fixture in f["fixtures"]:
  key=fixture["logicalKey"]
  if key not in docs: errors.append(f"fixture {fixture['id']} missing logicalKey {key}"); continue
  p,doc=docs[key]
  if doc.get("_id")!=fixture["expectedId"]: errors.append(f"fixture {fixture['id']} stable ID changed")
  if registry["documents"].get(key)!=fixture["expectedId"]: errors.append(f"fixture {fixture['id']} registry ID changed")
  for dotted,expected in fixture.get("expected",{}).items():
   try: actual=get_path(doc,dotted)
   except (KeyError,TypeError): errors.append(f"fixture {fixture['id']} missing {dotted}"); continue
   if actual!=expected: errors.append(f"fixture {fixture['id']} {dotted}: {actual!r} != {expected!r}")
  if "embeddedActorItemKeys" in fixture.get("specialChecks",[]):
   actor=doc["_id"]
   for item in doc.get("items",[]):
    iid=item.get("_id"); expected=f"!actors.items!{actor}.{iid}"
    if item.get("_key")!=expected: errors.append(f"fixture {fixture['id']} embedded Item {iid} _key mismatch")
 if errors:
  print("Edgeheart maintenance regression validation FAILED")
  for e in errors: print(f" - {e}")
  return 1
 print("Edgeheart maintenance regression validation PASS")
 print(f" - source documents: {len(docs)}")
 print(f" - structural folders: {folders}")
 print(f" - source pack entries: {sum(entries_by_pack.values())}")
 print(f" - regression fixtures: {len(f['fixtures'])}")
 print(f" - deployment assets: {len(assets['entries'])}")
 print(" - Domain Cards: 231 (21 per Competency)")
 return 0
if __name__=="__main__": raise SystemExit(main())
