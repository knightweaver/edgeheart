#!/usr/bin/env python3
"""Validate Edgeheart Step 4 resolved references against Daggerheart 2.10.5 shapes."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

MODULE = "edgeheart"
PACK_BY_PREFIX = {
    "feature": "edgeheart-features",
    "class": "edgeheart-classes",
    "subclass": "edgeheart-subclasses",
    "ancestry": "edgeheart-ancestries",
    "community": "edgeheart-communities",
}
EXPECTED_KINDS = {
    "bundle-symbolic-reference": 118,
    "external-domain-registration-reference": 9,
}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def uuid_for(key: str, registry: dict[str, str]) -> str:
    pfx = key.split(":", 1)[0]
    pack = PACK_BY_PREFIX[pfx]
    return f"Compendium.{MODULE}.{pack}.Item.{registry[key]}"

def index_docs(repo: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    out = {}
    for path in sorted((repo / "src/packs").rglob("*.json")):
        doc = load(path)
        if str(doc.get("_key", "")).startswith("!folders!"):
            continue
        key = (
            doc.get("flags", {})
            .get("edgeheart", {})
            .get("deployment", {})
            .get("logicalKey")
        )
        if key:
            out[key] = (path, doc)
    return out

def find_symbolic(value: Any, path: str = "$") -> list[str]:
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            p = f"{path}.{key}"
            if key == "ref" and isinstance(child, str):
                found.append(f"{p}={child}")
            else:
                found.extend(find_symbolic(child, p))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found.extend(find_symbolic(child, f"{path}[{i}]"))
    elif isinstance(value, str):
        if value.startswith("@class:") or value.startswith(
            ("feature:", "class:", "subclass:", "ancestry:", "community:")
        ):
            found.append(f"{path}={value}")
    return found

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args()
    repo = args.repo.resolve()
    errors = []

    registry = load(repo / "build/step3/stable-id-registry.json")["documents"]
    relations = load(repo / "build/step3/bundle-relations.json")
    step3_unresolved = load(repo / "build/step3/unresolved-references.json")
    resolution = load(repo / "build/step4/resolution-map.json")
    summary = load(repo / "build/step4/step4-summary.json")
    docs = index_docs(repo)

    if len(docs) != 638:
        errors.append(f"expected 638 indexed source documents, got {len(docs)}")

    if resolution.get("count") != 127 or len(resolution.get("references", [])) != 127:
        errors.append("Step 4 resolution map must contain exactly 127 references")

    kinds = Counter(r["kind"] for r in resolution.get("references", []))
    if dict(kinds) != EXPECTED_KINDS:
        errors.append(f"unexpected Step 4 resolution-kind counts: {dict(kinds)}")

    step3_keys = Counter(
        (r["ownerLogicalKey"], r["targetLogicalKey"], r["kind"])
        for r in step3_unresolved["references"]
    )
    step4_keys = Counter(
        (r["ownerLogicalKey"], r["targetLogicalKey"], r["kind"])
        for r in resolution["references"]
    )
    if step3_keys != step4_keys:
        errors.append("Step 4 does not account one-for-one for the Step 3 unresolved inventory")

    # Validate every class and its subclasses.
    for class_key, relation in relations["classes"].items():
        _, cls = docs[class_key]
        pending = relation["pendingDomains"]
        if cls["system"].get("domains") != pending:
            errors.append(
                f"{class_key}: domains {cls['system'].get('domains')} != expected {pending}"
            )
        if cls.get("flags", {}).get("edgeheart", {}).get("pendingDomainMapping") is not None:
            errors.append(f"{class_key}: pendingDomainMapping should be removed after Step 4")

        if "subclasses" in cls["system"]:
            errors.append(f"{class_key}: obsolete subclasses field present")

        for link in cls["system"].get("features", []):
            if set(link) != {"type", "item"}:
                errors.append(f"{class_key}: class feature link shape must be type+item")
            elif not str(link["item"]).startswith("Compendium.edgeheart.edgeheart-features.Item."):
                errors.append(f"{class_key}: invalid feature Compendium UUID {link['item']}")

        dep = cls.get("flags", {}).get("edgeheart", {}).get("deployment", {})
        if dep.get("sourceBuildStep") != 4 or dep.get("referencesResolved") is not True:
            errors.append(f"{class_key}: deployment state not resolved at Step 4")
        if dep.get("domainRegistrationPending") is not True:
            errors.append(f"{class_key}: domainRegistrationPending must remain true")

        linked_class = uuid_for(class_key, registry)
        for subclass_key in relation["subclasses"]:
            _, sub = docs[subclass_key]
            if sub["system"].get("linkedClass") != linked_class:
                errors.append(f"{subclass_key}: linkedClass mismatch")
            for link in sub["system"].get("features", []):
                if set(link) != {"type", "item"}:
                    errors.append(f"{subclass_key}: subclass feature link shape must be type+item")
                elif not str(link["item"]).startswith(
                    "Compendium.edgeheart.edgeheart-features.Item."
                ):
                    errors.append(f"{subclass_key}: invalid feature UUID {link['item']}")
            dep = sub.get("flags", {}).get("edgeheart", {}).get("deployment", {})
            if dep.get("sourceBuildStep") != 4 or dep.get("referencesResolved") is not True:
                errors.append(f"{subclass_key}: deployment state not resolved at Step 4")

    # Validate Life Paths and Affiliations.
    for parent_key, relation in relations["origins"].items():
        _, parent = docs[parent_key]
        expected = [uuid_for(k, registry) for k in relation["features"]]
        if parent_key.startswith("ancestry:"):
            actual = [link.get("item") for link in parent["system"].get("features", [])]
            if any(set(link) != {"type", "item"} for link in parent["system"].get("features", [])):
                errors.append(f"{parent_key}: ancestry feature links must be type+item")
        else:
            actual = parent["system"].get("features", [])
        if actual != expected:
            errors.append(f"{parent_key}: resolved origin feature UUIDs do not match bundle")
        dep = parent.get("flags", {}).get("edgeheart", {}).get("deployment", {})
        if dep.get("sourceBuildStep") != 4 or dep.get("referencesResolved") is not True:
            errors.append(f"{parent_key}: deployment state not resolved at Step 4")

    # No symbolic bundle references may remain in source documents.
    symbolic = []
    for key, (path, doc) in docs.items():
        hits = find_symbolic(doc.get("system", {}))
        for hit in hits:
            symbolic.append(f"{path.relative_to(repo)}: {hit}")
    if symbolic:
        errors.append(f"symbolic references remain after Step 4: {symbolic[:10]}")

    # Every resolution-map Compendium UUID must target the exact stable ID.
    for record in resolution["references"]:
        target = record["targetLogicalKey"]
        value = record["resolvedValue"]
        if target.startswith("domain:"):
            if value != target.split(":", 1)[1]:
                errors.append(f"bad resolved domain value for {target}: {value}")
        else:
            expected = uuid_for(target, registry)
            if value != expected:
                errors.append(f"bad resolved UUID for {target}: {value} != {expected}")

    if summary.get("status") != "PASS":
        errors.append("step4-summary status is not PASS")
    if summary.get("domainRuntimeRegistrationPending") is not True:
        errors.append("Step 4 must leave runtime domain registration pending")
    if summary.get("artPathRewritePending") is not True:
        errors.append("Step 4 must leave art-path rewriting pending")
    if summary.get("compendiumCompilationPending") is not True:
        errors.append("Step 4 must leave Compendium compilation pending")

    if errors:
        print("Edgeheart Step 4 reference validation FAILED", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("Edgeheart Step 4 reference validation PASS")
    print(" - resolved references: 127")
    print(" - classes: 9")
    print(" - subclasses: 18")
    print(" - life paths: 6")
    print(" - affiliations: 8")
    print(" - symbolic references remaining: 0")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
