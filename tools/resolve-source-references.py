#!/usr/bin/env python3
"""Step 4: resolve Edgeheart symbolic bundle references into Foundry UUIDs.

Consumes the authoritative Step 3 source tree and reports:
- build/step3/stable-id-registry.json
- build/step3/bundle-relations.json
- build/step3/unresolved-references.json

Produces:
- resolved class feature/subclass/domain links
- resolved subclass feature/linked-class links
- resolved ancestry/community feature links
- build/step4/resolution-map.json
- build/step4/step4-summary.json
- build/step4/STEP-4-REPORT.md

This step deliberately does NOT register Homebrew domains at runtime, rewrite
art paths, or compile LevelDB Compendia.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

MODULE_ID = "edgeheart"

PACK_BY_PREFIX = {
    "feature": "edgeheart-features",
    "class": "edgeheart-classes",
    "subclass": "edgeheart-subclasses",
    "ancestry": "edgeheart-ancestries",
    "community": "edgeheart-communities",
}

EXPECTED_STEP3_UNRESOLVED = {
    "bundle-symbolic-reference": 118,
    "external-domain-registration-reference": 9,
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def write_doc(path: Path, doc: dict[str, Any]) -> None:
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def prefix(logical_key: str) -> str:
    return logical_key.split(":", 1)[0]

def compendium_uuid(logical_key: str, registry: dict[str, str]) -> str:
    pfx = prefix(logical_key)
    pack = PACK_BY_PREFIX.get(pfx)
    if not pack:
        raise ValueError(f"No Compendium mapping for logical key: {logical_key}")
    doc_id = registry.get(logical_key)
    if not doc_id:
        raise ValueError(f"Logical key missing from stable ID registry: {logical_key}")
    return f"Compendium.{MODULE_ID}.{pack}.Item.{doc_id}"

def deployment(doc: dict[str, Any]) -> dict[str, Any]:
    return doc.setdefault("flags", {}).setdefault("edgeheart", {}).setdefault("deployment", {})

def build_index(repo: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted((repo / "src/packs").rglob("*.json")):
        doc = load_json(path)
        if str(doc.get("_key", "")).startswith("!folders!"):
            continue
        key = (
            doc.get("flags", {})
            .get("edgeheart", {})
            .get("deployment", {})
            .get("logicalKey")
        )
        if not key:
            raise ValueError(f"Missing deployment.logicalKey: {path.relative_to(repo)}")
        if key in index:
            raise ValueError(f"Duplicate logical key in source tree: {key}")
        index[key] = path
    return index

def resolve_link_array(
    links: list[dict[str, Any]],
    registry: dict[str, str],
    owner: str,
    records: list[dict[str, Any]],
) -> None:
    for i, link in enumerate(links):
        ref = link.get("ref")
        if not ref:
            if "item" in link:
                continue
            raise ValueError(f"{owner} feature link {i} has neither ref nor item")
        value = compendium_uuid(ref, registry)
        link.pop("ref", None)
        link["item"] = value
        records.append({
            "ownerLogicalKey": owner,
            "jsonPath": f"$.system.features[{i}]",
            "targetLogicalKey": ref,
            "resolvedValue": value,
            "kind": "bundle-symbolic-reference",
        })

def assert_step3_inventory(unresolved: dict[str, Any]) -> None:
    refs = unresolved.get("references", [])
    if unresolved.get("count") != 127 or len(refs) != 127:
        raise ValueError(f"Expected 127 Step 3 unresolved references, got {len(refs)}")
    counts = Counter(r.get("kind") for r in refs)
    if dict(counts) != EXPECTED_STEP3_UNRESOLVED:
        raise ValueError(f"Unexpected Step 3 unresolved-reference counts: {dict(counts)}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    step3 = repo / "build/step3"
    registry_doc = load_json(step3 / "stable-id-registry.json")
    relations = load_json(step3 / "bundle-relations.json")
    unresolved = load_json(step3 / "unresolved-references.json")
    registry: dict[str, str] = registry_doc["documents"]

    assert_step3_inventory(unresolved)
    index = build_index(repo)

    if set(index) != set(registry):
        missing = sorted(set(registry) - set(index))
        extra = sorted(set(index) - set(registry))
        raise ValueError(
            f"Source tree / stable registry mismatch; missing={missing[:5]} extra={extra[:5]}"
        )

    records: list[dict[str, Any]] = []

    # Resolve Class and Subclass relationships.
    for class_key, relation in sorted(relations["classes"].items()):
        class_path = index[class_key]
        class_doc = load_json(class_path)

        pending_domains = list(relation.get("pendingDomains", []))
        if not pending_domains:
            raise ValueError(f"{class_key} has no pending Competency/domain mapping")
        class_doc["system"]["domains"] = pending_domains

        edgeheart_flags = class_doc.setdefault("flags", {}).setdefault("edgeheart", {})
        source_pending = edgeheart_flags.get("pendingDomainMapping", pending_domains)
        if list(source_pending) != pending_domains:
            raise ValueError(
                f"{class_key} pendingDomainMapping does not match bundle relation: "
                f"{source_pending} vs {pending_domains}"
            )
        edgeheart_flags.pop("pendingDomainMapping", None)

        for domain in pending_domains:
            records.append({
                "ownerLogicalKey": class_key,
                "jsonPath": "$.system.domains[]",
                "targetLogicalKey": f"domain:{domain}",
                "resolvedValue": domain,
                "kind": "external-domain-registration-reference",
            })

        resolve_link_array(
            class_doc["system"].get("features", []),
            registry,
            class_key,
            records,
        )

        subclass_keys = list(relation.get("subclasses", []))
        class_doc["system"].pop("subclasses", None)

        dep = deployment(class_doc)
        dep.update({
            "sourceBuildStep": 4,
            "referencesResolved": True,
            "resolvedDomains": pending_domains,
            "domainRegistrationPending": True,
        })
        write_doc(class_path, class_doc)

        # Every subclass listed in the class bundle gets feature UUIDs and a
        # linkedClass UUID back to this parent class.
        linked_class_uuid = compendium_uuid(class_key, registry)
        for subclass_key in subclass_keys:
            subclass_path = index[subclass_key]
            subclass_doc = load_json(subclass_path)

            resolve_link_array(
                subclass_doc["system"].get("features", []),
                registry,
                subclass_key,
                records,
            )

            previous = subclass_doc["system"].get("linkedClass")
            expected_symbolic = f"@{class_key}"
            if previous not in (expected_symbolic, linked_class_uuid):
                raise ValueError(
                    f"{subclass_key} linkedClass mismatch: "
                    f"expected {expected_symbolic!r}, got {previous!r}"
                )
            if previous != linked_class_uuid:
                records.append({
                    "ownerLogicalKey": subclass_key,
                    "jsonPath": "$.system.linkedClass",
                    "targetLogicalKey": class_key,
                    "resolvedValue": linked_class_uuid,
                    "kind": "bundle-symbolic-reference",
                })
            subclass_doc["system"]["linkedClass"] = linked_class_uuid

            sdep = deployment(subclass_doc)
            sdep.update({
                "sourceBuildStep": 4,
                "referencesResolved": True,
            })
            write_doc(subclass_path, subclass_doc)

    # Resolve Life Path (ancestry) and Affiliation (community) feature links.
    for parent_key, relation in sorted(relations["origins"].items()):
        parent_path = index[parent_key]
        parent_doc = load_json(parent_path)
        feature_keys = list(relation.get("features", []))

        if parent_key.startswith("ancestry:"):
            links = parent_doc["system"].get("features", [])
            if len(links) != len(feature_keys):
                raise ValueError(
                    f"{parent_key} feature count mismatch: {len(links)} vs {len(feature_keys)}"
                )
            resolve_link_array(links, registry, parent_key, records)

        elif parent_key.startswith("community:"):
            current = parent_doc["system"].get("features", [])
            if len(current) != len(feature_keys):
                raise ValueError(
                    f"{parent_key} feature count mismatch: {len(current)} vs {len(feature_keys)}"
                )
            resolved: list[str] = []
            for i, (value, target_key) in enumerate(zip(current, feature_keys)):
                expected = target_key
                if value not in (expected, compendium_uuid(target_key, registry)):
                    raise ValueError(
                        f"{parent_key} feature {i} mismatch: expected {expected!r}, got {value!r}"
                    )
                uuid = compendium_uuid(target_key, registry)
                resolved.append(uuid)
                if value != uuid:
                    records.append({
                        "ownerLogicalKey": parent_key,
                        "jsonPath": f"$.system.features[{i}]",
                        "targetLogicalKey": target_key,
                        "resolvedValue": uuid,
                        "kind": "bundle-symbolic-reference",
                    })
            parent_doc["system"]["features"] = resolved
        else:
            raise ValueError(f"Unknown origin parent type: {parent_key}")

        pdep = deployment(parent_doc)
        pdep.update({
            "sourceBuildStep": 4,
            "referencesResolved": True,
        })
        write_doc(parent_path, parent_doc)

    # Step 4 must account one-for-one for the exact Step 3 unresolved inventory.
    expected_tuples = Counter(
        (r["ownerLogicalKey"], r["targetLogicalKey"], r["kind"])
        for r in unresolved["references"]
    )
    actual_tuples = Counter(
        (r["ownerLogicalKey"], r["targetLogicalKey"], r["kind"])
        for r in records
    )
    if actual_tuples != expected_tuples:
        missing = list((expected_tuples - actual_tuples).elements())[:10]
        extra = list((actual_tuples - expected_tuples).elements())[:10]
        raise ValueError(f"Resolution accounting mismatch; missing={missing} extra={extra}")

    if len(records) != 127:
        raise ValueError(f"Expected 127 resolution records, got {len(records)}")

    step4 = repo / "build/step4"
    step4.mkdir(parents=True, exist_ok=True)

    kinds = Counter(r["kind"] for r in records)
    resolution_map = {
        "schemaVersion": "1.0",
        "buildStep": 4,
        "sourceStep": 3,
        "status": "RESOLVED",
        "count": len(records),
        "references": sorted(
            records,
            key=lambda r: (
                r["ownerLogicalKey"],
                r["jsonPath"],
                r["targetLogicalKey"],
            ),
        ),
    }
    dump_json(step4 / "resolution-map.json", resolution_map)

    summary = {
        "step": 4,
        "status": "PASS",
        "resolvedReferenceCount": len(records),
        "resolvedKinds": dict(sorted(kinds.items())),
        "classesResolved": len(relations["classes"]),
        "subclassesResolved": sum(
            len(v.get("subclasses", [])) for v in relations["classes"].values()
        ),
        "lifePathsResolved": sum(
            1 for k in relations["origins"] if k.startswith("ancestry:")
        ),
        "affiliationsResolved": sum(
            1 for k in relations["origins"] if k.startswith("community:")
        ),
        "classDomainsPopulated": len(relations["classes"]),
        "domainRuntimeRegistrationPending": True,
        "artPathRewritePending": True,
        "compendiumCompilationPending": True,
        "nextStep": (
            "Register the eleven Edgeheart Competencies through Daggerheart 2.10.5 "
            "Homebrew domains before runtime qualification."
        ),
    }
    dump_json(step4 / "step4-summary.json", summary)

    (step4 / "STEP-4-REPORT.md").write_text(
        "# Edgeheart Foundry Build — Step 4 Report\n\n"
        "**Status:** PASS\n\n"
        f"- Resolved references: **{len(records)}**\n"
        f"- Classes resolved: **{summary['classesResolved']}**\n"
        f"- Subclasses resolved: **{summary['subclassesResolved']}**\n"
        f"- Life Paths resolved: **{summary['lifePathsResolved']}**\n"
        f"- Affiliations resolved: **{summary['affiliationsResolved']}**\n"
        f"- Class Competency mappings populated: **{summary['classDomainsPopulated']}**\n"
        "- Daggerheart Homebrew Competency registration: **pending downstream step**\n"
        "- Final art-path rewriting: **pending downstream step**\n"
        "- LevelDB Compendium compilation: **pending downstream step**\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
