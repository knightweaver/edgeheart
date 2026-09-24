#!/usr/bin/env python3
"""Compare DH2 Environment projection against the frozen source archive."""
import argparse
import html
import json
import zipfile
from pathlib import Path

EXTERNAL={"Cordon Eidolon", "Handler's Hound", "Blackwall Seraph"}

def old_text(value):
    value=value.replace("</p><p>","\n\n").replace("<br>","\n")
    return html.unescape(value.replace("<p>","").replace("</p>",""))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,default=Path.cwd())
    repo=parser.parse_args().repo.resolve()
    archive=repo/"sources/edgeheart-consolidated-production-v1.0.zip"
    envs={json.loads(p.read_text())["name"]:json.loads(p.read_text()) for p in
          (repo/"src/packs/adventures/environments").glob("environment_*.json")}
    adversaries={d["name"]:d["_id"] for p in (repo/"src/packs/adventures/adversaries").glob("adversary_*.json")
                 if (d:=json.loads(p.read_text()))}
    assert len(envs)==15 and len(adversaries)==22
    features=external=0
    with zipfile.ZipFile(archive) as z:
        source_paths=[p for p in z.namelist() if "/foundry/direct/environments/" in p and p.endswith(".foundry.json")]
        assert len(source_paths)==15
        for path in source_paths:
            legacy=json.loads(z.read(path)); actual=envs[legacy["name"]]
            assert "features" not in actual["system"],actual["name"]
            assert actual["system"]["impulses"]==", ".join(legacy["system"]["impulses"]),actual["name"]
            old_features=legacy["system"]["features"]; new_features=actual["items"]
            assert len(old_features)==len(new_features),actual["name"]
            for old,new in zip(old_features,new_features):
                assert (new["_id"],new["name"],new["img"],new["type"]) == (old["_id"],old["name"],old["img"],"feature")
                assert new["_key"]==f"!actors.items!{actual['_id']}.{old['_id']}"
                assert new["system"]["featureForm"]==old["actionType"]
                assert old_text(new["system"]["description"])==old["description"]
                features+=1
            groups=list(actual["system"]["potentialAdversaries"].values())
            assert [g["label"] for g in groups]==legacy["system"]["potentialAdversaries"],actual["name"]
            for group in groups:
                actor_id=adversaries.get(group["label"])
                if actor_id:
                    assert group["adversaries"]==[f"Compendium.edgeheart.edgeheart-adversaries.Actor.{actor_id}"]
                else:
                    assert group["label"] in EXTERNAL and group["adversaries"]==[]
                    external+=1
    assert features==49 and external==5,(features,external)
    print(f"Edgeheart DH2 Environment projection PASS: {len(envs)} Environments, {features} embedded Features, {external} external named suggestions")

if __name__=="__main__": main()
