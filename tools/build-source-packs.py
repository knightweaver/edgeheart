#!/usr/bin/env python3
"""Step 3: build deterministic Edgeheart Foundry source-pack JSON.

This step assigns stable IDs, lays out source packs/folders, and inventories bundle
references. It deliberately does not resolve bundle refs, register Competencies,
rewrite final art paths, or compile LevelDB packs.
"""
from __future__ import annotations

import argparse, copy, hashlib, json, re, shutil, sys, zipfile
from collections import Counter
from pathlib import Path
from typing import Any

PACKAGE="edgeheart-consolidated-production-v1.0"
CORE="13.351"; SYSTEM="daggerheart"; SYSTEM_VERSION="1.2.7"; MODULE="edgeheart"
NS="edgeheart-foundry-source-v1"
PACKS={
 "weapons":("src/packs/items/weapons","edgeheart-weapons","Item"),
 "armors":("src/packs/items/armors","edgeheart-armors","Item"),
 "loot":("src/packs/items/loot","edgeheart-loot","Item"),
 "consumables":("src/packs/items/consumables","edgeheart-consumables","Item"),
 "cyberware":("src/packs/items/cyberware","edgeheart-cyberware","Item"),
 "classes":("src/packs/system/classes","edgeheart-classes","Item"),
 "subclasses":("src/packs/system/subclasses","edgeheart-subclasses","Item"),
 "domains":("src/packs/system/domains","edgeheart-domains","Item"),
 "features":("src/packs/system/features","edgeheart-features","Item"),
 "ancestries":("src/packs/system/ancestries","edgeheart-ancestries","Item"),
 "communities":("src/packs/system/communities","edgeheart-communities","Item"),
 "adversaries":("src/packs/adventures/adversaries","edgeheart-adversaries","Actor"),
 "environments":("src/packs/adventures/environments","edgeheart-environments","Actor"),
}
DIRECT={"weapons":"weapons","armors":"armors","loot":"loot","consumables":"consumables",
        "cyberware":"cyberware","domain-cards":"domains","adversaries":"adversaries","environments":"environments"}
EXPECTED_DIRECT={"weapons":64,"armors":25,"loot":40,"consumables":40,"cyberware":60,"domain-cards":231,"environments":15,"adversaries":22}
EXPECTED_DOCS={"weapons":64,"armors":25,"loot":40,"consumables":40,"cyberware":60,"domains":231,
               "classes":9,"subclasses":18,"features":100,"ancestries":6,"communities":8,"environments":15,"adversaries":22}
SYMBOLIC=("feature:","class:","subclass:","ancestry:","community:")

def sid(key:str)->str: return hashlib.sha256(f"{NS}:{key}".encode()).hexdigest()[:16]
def safe(s:str)->str: return re.sub(r"[^A-Za-z0-9]+","_",s).strip("_") or "Unnamed"
def dump(p:Path,v:Any): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def pdir(repo:Path,key:str)->Path: return repo/PACKS[key][0]
def stats(): return {"compendiumSource":None,"duplicateSource":None,"exportSource":None,"coreVersion":CORE,"systemId":SYSTEM,"systemVersion":SYSTEM_VERSION,"lastModifiedBy":None}

def root_of(z:zipfile.ZipFile)->str:
 e=f"{PACKAGE}/MANIFEST.json"
 if e in z.namelist(): return f"{PACKAGE}/"
 c=[n[:-len("MANIFEST.json")] for n in z.namelist() if n.endswith("/MANIFEST.json")]
 if len(c)!=1: raise ValueError("Could not identify consolidated package root")
 return c[0]

def finish(doc:dict,key:str,pack:str,folder:str|None=None)->dict:
 d=copy.deepcopy(doc); i=sid(f"document:{key}"); d["_id"]=i; d["folder"]=folder if folder is not None else d.get("folder")
 d.setdefault("sort",0); d.setdefault("ownership",{"default":0}); d.setdefault("effects",[]); d.setdefault("flags",{}); d["_stats"]=stats()
 d["_key"]=f"!{'actors' if PACKS[pack][2]=='Actor' else 'items'}!{i}"
 dep=d["flags"].setdefault("edgeheart",{}).setdefault("deployment",{})
 dep.update({"logicalKey":key,"sourceBuildStep":3,"referencesResolved":not key.startswith(("class:","subclass:","ancestry:","community:"))})
 return d

def folder(name:str,key:str,parent:str|None=None)->dict:
 i=sid(f"folder:{key}")
 return {"type":"Item","folder":parent,"name":name,"color":None,"sorting":"a","_id":i,"description":"","sort":0,
         "flags":{"edgeheart":{"deployment":{"logicalKey":f"folder:{key}","sourceBuildStep":3}}},"_stats":stats(),"_key":f"!folders!{i}"}

def write(repo:Path,pack:str,d:dict):
 pre="folders" if d["_key"].startswith("!folders!") else d["type"]
 dump(pdir(repo,pack)/f"{pre}_{safe(d.get('name','Unnamed'))}_{d['_id']}.json",d)

def refs(v:Any,path="$"):
 out=[]
 if isinstance(v,dict):
  for k,x in v.items():
   q=f"{path}.{k}"
   if k=="ref" and isinstance(x,str) and x.startswith(SYMBOLIC): out.append((q,x))
   else: out.extend(refs(x,q))
 elif isinstance(v,list):
  for n,x in enumerate(v):
   q=f"{path}[{n}]"
   if isinstance(x,str) and x.startswith(SYMBOLIC): out.append((q,x))
   else: out.extend(refs(x,q))
 elif isinstance(v,str) and v.startswith("@class:"): out.append((path,v[1:]))
 return out

def direct_key(cat:str,rel:str,d:dict)->str:
 src=d.get("flags",{}).get("edgeheart",{}).get("source",{}); slug=src.get("slug") or Path(rel).name.replace(".foundry.json","")
 if cat=="domain-cards": return f"domainCard:{d['system']['domain']}:{slug}"
 typ=src.get("entityType") or {"weapons":"weapon","armors":"armor","loot":"loot","consumables":"consumable","cyberware":"cyberware","adversaries":"adversary","environments":"environment"}[cat]
 return f"{typ}:{slug}"

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("package",type=Path); ap.add_argument("--repo",type=Path,default=Path.cwd()); a=ap.parse_args()
 arc=a.package.resolve(); repo=a.repo.resolve(); report=repo/"build/step3"
 if not arc.exists(): raise FileNotFoundError(arc)
 if json.loads((repo/"module.json").read_text())["id"]!=MODULE: raise ValueError("Not an Edgeheart repo")
 arc_hash=hashlib.sha256(arc.read_bytes()).hexdigest()
 for k in PACKS:
  q=pdir(repo,k); q.mkdir(parents=True,exist_ok=True)
  for f in q.glob("*.json"): f.unlink()
  if (q/".gitkeep").exists(): (q/".gitkeep").unlink()
 if report.exists(): shutil.rmtree(report)
 report.mkdir(parents=True)
 registry={}; folders={}; unresolved=[]; relations={"classes":{},"origins":{}}; counts=Counter(); fcounts=Counter(); dcounts=Counter()
 def reg(key,pack,d):
  if key in registry: raise ValueError(f"Duplicate logical key: {key}")
  if d["_id"] in registry.values(): raise ValueError(f"Stable ID collision: {d['_id']}")
  registry[key]=d["_id"]
 def mk(pack,name,key,parent=None):
  lk=f"{pack}:{key}"
  if lk in folders: return folders[lk]
  par=folders.get(f"{pack}:{parent}") if parent else None
  if parent and not par: raise ValueError(f"Missing folder parent {parent}")
  d=folder(name,lk,par); write(repo,pack,d); folders[lk]=d["_id"]; fcounts[pack]+=1; return d["_id"]
 with zipfile.ZipFile(arc) as z:
  root=root_of(z); man=json.loads(z.read(root+"MANIFEST.json")); runtime=man["foundry"]["targetRuntime"]
  if man.get("packageVersion")!="1.0" or runtime!={"foundryCore":CORE,"systemId":SYSTEM,"systemVersion":SYSTEM_VERSION}: raise ValueError("Package/runtime mismatch")
  for t in range(1,5): mk("weapons",f"Tier {t}",f"tier-{t}"); mk("armors",f"Tier {t}",f"tier-{t}")
  cards=[n for n in z.namelist() if "/foundry/direct/domain-cards/" in n and n.endswith(".foundry.json")]
  domains=sorted({n.split("/foundry/direct/domain-cards/",1)[1].split("/",1)[0] for n in cards})
  if len(domains)!=11: raise ValueError(f"Expected 11 Competencies, got {len(domains)}")
  for dom in domains:
   mk("domains",dom.replace("-"," ").title(),f"domain-{dom}")
   for lvl in range(1,11): mk("domains",f"Level {lvl}",f"domain-{dom}-level-{lvl}",f"domain-{dom}")
  mk("features","Class and Subclass Features","class-subclass-features"); mk("features","Origin Features","origin-features")
  pref=root+"foundry/direct/"
  for n in sorted(x for x in z.namelist() if x.startswith(pref) and x.endswith(".foundry.json")):
   rel=n[len(pref):]; cat=rel.split("/",1)[0]; pack=DIRECT[cat]; raw=json.loads(z.read(n)); key=direct_key(cat,rel,raw); fid=None
   if cat in ("weapons","armors"): fid=folders[f"{pack}:tier-{int(raw['system']['tier'])}"]
   elif cat=="domain-cards": fid=folders[f"domains:domain-{raw['system']['domain']}-level-{int(raw['system']['level'])}"]
   d=finish(raw,key,pack,fid); write(repo,pack,d); reg(key,pack,d); counts[pack]+=1; dcounts[cat]+=1
  if dict(dcounts)!=EXPECTED_DIRECT: raise ValueError(f"Direct counts mismatch: {dict(dcounts)}")
  cp=root+"foundry/bundles/classes/"; class_paths=sorted(n for n in z.namelist() if n.startswith(cp) and n.endswith(".bundle.json"))
  if len(class_paths)!=9: raise ValueError("Expected 9 class bundles")
  for n in class_paths:
   b=json.loads(z.read(n)); ce=b["class"]; ck=ce["key"]; cslug=ck.split(":",1)[1]; owners={cslug:f"class-{cslug}"}; mk("features",ce["document"]["name"],owners[cslug],"class-subclass-features")
   for se in b["subclasses"]:
    sk=se["key"]; ss=sk.split(":",1)[1]; owners[ss]=f"subclass-{ss}"; mk("features",se["document"]["name"],owners[ss],"class-subclass-features")
   fkeys=[]
   for fe in b["creationOrder"]:
    key=fe["key"]; owner=key.split(":",2)[1]; d=finish(fe["document"],key,"features",folders[f"features:{owners[owner]}"]); write(repo,"features",d); reg(key,"features",d); counts["features"]+=1; fkeys.append(key)
   cd=finish(ce["document"],ck,"classes"); write(repo,"classes",cd); reg(ck,"classes",cd); counts["classes"]+=1
   skeys=[]; sdocs=[]
   for se in b["subclasses"]:
    sk=se["key"]; sd=finish(se["document"],sk,"subclasses"); write(repo,"subclasses",sd); reg(sk,"subclasses",sd); counts["subclasses"]+=1; skeys.append(sk); sdocs.append((sk,sd))
   pending=cd.get("flags",{}).get("edgeheart",{}).get("pendingDomainMapping",[]); relations["classes"][ck]={"bundle":Path(n).name,"features":fkeys,"subclasses":skeys,"pendingDomains":pending}
   for owner,d in [(ck,cd),*sdocs]:
    for loc,target in refs(d): unresolved.append({"ownerLogicalKey":owner,"jsonPath":loc,"targetLogicalKey":target,"kind":"bundle-symbolic-reference","bundle":Path(n).name})
   for sk in skeys: unresolved.append({"ownerLogicalKey":ck,"jsonPath":"$.system.subclasses[]","targetLogicalKey":sk,"kind":"bundle-membership-reference","bundle":Path(n).name})
   for dom in pending: unresolved.append({"ownerLogicalKey":ck,"jsonPath":"$.system.domains[]","targetLogicalKey":f"domain:{dom}","kind":"external-domain-registration-reference","bundle":Path(n).name})
  op=root+"foundry/bundles/origins/"; origin_paths=sorted(n for n in z.namelist() if n.startswith(op) and n.endswith(".bundle.json"))
  if len(origin_paths)!=14: raise ValueError("Expected 14 origin bundles")
  for n in origin_paths:
   b=json.loads(z.read(n)); pe=b["parent"]; pk=pe["key"]; slug=pk.split(":",1)[1]; fk=f"origin-{slug}"; mk("features",pe["document"]["name"],fk,"origin-features"); fkeys=[]
   for fe in b["creationOrder"]:
    key=fe["key"]; d=finish(fe["document"],key,"features",folders[f"features:{fk}"]); write(repo,"features",d); reg(key,"features",d); counts["features"]+=1; fkeys.append(key)
   pack="ancestries" if pk.startswith("ancestry:") else "communities"; pd=finish(pe["document"],pk,pack); write(repo,pack,pd); reg(pk,pack,pd); counts[pack]+=1
   relations["origins"][pk]={"bundle":Path(n).name,"originKind":b.get("originKind"),"features":fkeys}
   for loc,target in refs(pd): unresolved.append({"ownerLogicalKey":pk,"jsonPath":loc,"targetLogicalKey":target,"kind":"bundle-symbolic-reference","bundle":Path(n).name})
 if dict(counts)!=EXPECTED_DOCS: raise ValueError(f"Document counts mismatch: {dict(counts)}")
 if len(registry)!=638 or len(folders)!=172: raise ValueError("Registry/folder count mismatch")
 if len(set([*registry.values(),*folders.values()]))!=810: raise ValueError("Stable ID collision")
 unknown=[r for r in unresolved if not r["targetLogicalKey"].startswith("domain:") and r["targetLogicalKey"] not in registry]
 if unknown: raise ValueError(f"Unknown internal refs: {unknown[:3]}")
 for k in PACKS:
  for f in pdir(repo,k).glob("*.json"):
   d=json.loads(f.read_text()); a=d.get("system",{}).get("actions")
   if a is not None and not isinstance(a,dict): raise ValueError(f"system.actions is not object: {f}")
 dump(report/"stable-id-registry.json",{"schemaVersion":"1.0","buildStep":3,"idNamespace":NS,"documents":dict(sorted(registry.items())),"folders":dict(sorted(folders.items()))})
 dump(report/"unresolved-references.json",{"schemaVersion":"1.0","buildStep":3,"status":"INTENTIONALLY_UNRESOLVED_FOR_STEP_4","count":len(unresolved),"references":sorted(unresolved,key=lambda x:(x["ownerLogicalKey"],x["jsonPath"],x["targetLogicalKey"]))})
 dump(report/"bundle-relations.json",{"schemaVersion":"1.0","buildStep":3,**relations})
 summary={"step":3,"status":"PASS","inputPackage":PACKAGE,"inputArchiveSha256":arc_hash,"runtime":{"foundryCore":CORE,"systemId":SYSTEM,"systemVersion":SYSTEM_VERSION},"documentCount":638,"folderCount":172,"documentsByPack":dict(sorted(counts.items())),"foldersByPack":dict(sorted(fcounts.items())),"unresolvedReferenceCount":len(unresolved),"unresolvedKinds":dict(sorted(Counter(r["kind"] for r in unresolved).items())),"unknownInternalReferenceTargets":0,"stableIdCollisions":0,"systemActionsShapeErrors":0,"nextStep":"Resolve bundle references and class domain mappings before Compendium compilation."}
 dump(report/"step3-summary.json",summary)
 (report/"STEP-3-REPORT.md").write_text(f"# Edgeheart Foundry Build — Step 3 Report\n\n**Status:** PASS\n\n- Generated Foundry documents: **638**\n- Generated structural folders: **172**\n- Unresolved references inventoried for Step 4: **{len(unresolved)}**\n- Unknown internal targets: **0**\n- Stable-ID collisions: **0**\n- `system.actions` shape errors: **0**\n\nStep 3 deliberately leaves bundle references, Competency registration, final art-path rewriting, and LevelDB compilation to downstream steps.\n",encoding="utf-8")
 print(json.dumps(summary,indent=2)); return 0

if __name__=="__main__":
 try: raise SystemExit(main())
 except Exception as e: print(f"ERROR: {e}",file=sys.stderr); raise
