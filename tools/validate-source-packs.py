#!/usr/bin/env python3
"""Validate Edgeheart Step 3 generated source packs without compiling them."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

EXPECTED_DOCS = {
    "src/packs/items/weapons": 64,
    "src/packs/items/armors": 25,
    "src/packs/items/loot": 40,
    "src/packs/items/consumables": 40,
    "src/packs/items/cyberware": 60,
    "src/packs/system/classes": 9,
    "src/packs/system/subclasses": 18,
    "src/packs/system/domains": 231,
    "src/packs/system/features": 100,
    "src/packs/system/ancestries": 6,
    "src/packs/system/communities": 8,
    "src/packs/adventures/adversaries": 22,
    "src/packs/adventures/environments": 15,
}
EXPECTED_FOLDERS = {
    "src/packs/items/weapons": 4,
    "src/packs/items/armors": 4,
    "src/packs/system/domains": 121,
    "src/packs/system/features": 43,
}
EXPECTED_UNRESOLVED_KINDS = {
    "bundle-membership-reference": 18,
    "bundle-symbolic-reference": 118,
    "external-domain-registration-reference": 9,
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors: list[str] = []

    registry_path = repo / "build/step3/stable-id-registry.json"
    unresolved_path = repo / "build/step3/unresolved-references.json"
    summary_path = repo / "build/step3/step3-summary.json"
    for path in (registry_path, unresolved_path, summary_path):
        if not path.exists():
            errors.append(f"missing Step 3 report artifact: {path.relative_to(repo)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    registry = load_json(registry_path)
    unresolved = load_json(unresolved_path)
    summary = load_json(summary_path)

    documents = registry.get("documents", {})
    folders = registry.get("folders", {})
    if len(documents) != 638:
        errors.append(f"registry document count: expected 638, got {len(documents)}")
    if len(folders) != 172:
        errors.append(f"registry folder count: expected 172, got {len(folders)}")

    ids = list(documents.values()) + list(folders.values())
    if len(ids) != len(set(ids)):
        errors.append("duplicate stable IDs detected")

    file_ids: set[str] = set()
    actual_docs = Counter()
    actual_folders = Counter()
    action_shape_errors: list[str] = []

    for rel in sorted(set(EXPECTED_DOCS) | set(EXPECTED_FOLDERS)):
        directory = repo / rel
        if not directory.is_dir():
            errors.append(f"missing pack directory: {rel}")
            continue
        for path in directory.glob("*.json"):
            try:
                doc = load_json(path)
            except Exception as exc:
                errors.append(f"invalid JSON {path.relative_to(repo)}: {exc}")
                continue
            doc_id = doc.get("_id")
            if not isinstance(doc_id, str) or len(doc_id) != 16:
                errors.append(f"invalid Foundry ID in {path.relative_to(repo)}: {doc_id!r}")
            elif doc_id in file_ids:
                errors.append(f"duplicate Foundry ID in source tree: {doc_id}")
            else:
                file_ids.add(doc_id)
            if str(doc.get("_key", "")).startswith("!folders!"):
                actual_folders[rel] += 1
            else:
                actual_docs[rel] += 1
                actions = doc.get("system", {}).get("actions")
                if actions is not None and not isinstance(actions, dict):
                    action_shape_errors.append(str(path.relative_to(repo)))

                if doc.get("type") in ("adversary", "environment"):
                    actor_id = doc.get("_id")
                    for item in doc.get("items", []) or []:
                        item_id = item.get("_id")
                        expected_key = f"!actors.items!{actor_id}.{item_id}"
                        if item.get("_key") != expected_key:
                            errors.append(
                                f"{path.relative_to(repo)}: embedded Item {item_id} "
                                f"_key must be {expected_key!r}, got {item.get('_key')!r}"
                            )
                        for effect in item.get("effects", []) or []:
                            effect_id = effect.get("_id")
                            expected_effect_key = (
                                f"!actors.items.effects!{actor_id}.{item_id}.{effect_id}"
                            )
                            if effect.get("_key") != expected_effect_key:
                                errors.append(
                                    f"{path.relative_to(repo)}: embedded Item effect {effect_id} "
                                    f"_key must be {expected_effect_key!r}, got {effect.get('_key')!r}"
                                )
                    for effect in doc.get("effects", []) or []:
                        effect_id = effect.get("_id")
                        expected_effect_key = f"!actors.effects!{actor_id}.{effect_id}"
                        if effect.get("_key") != expected_effect_key:
                            errors.append(
                                f"{path.relative_to(repo)}: embedded Actor effect {effect_id} "
                                f"_key must be {expected_effect_key!r}, got {effect.get('_key')!r}"
                            )

    for rel, expected in EXPECTED_DOCS.items():
        if actual_docs[rel] != expected:
            errors.append(f"{rel}: expected {expected} documents, got {actual_docs[rel]}")
    for rel, expected in EXPECTED_FOLDERS.items():
        if actual_folders[rel] != expected:
            errors.append(f"{rel}: expected {expected} folders, got {actual_folders[rel]}")

    expected_all_ids = set(documents.values()) | set(folders.values())
    if file_ids != expected_all_ids:
        missing = sorted(expected_all_ids - file_ids)
        extra = sorted(file_ids - expected_all_ids)
        errors.append(f"source tree / registry ID mismatch; missing={missing[:5]} extra={extra[:5]}")

    refs = unresolved.get("references", [])
    if unresolved.get("count") != 145 or len(refs) != 145:
        errors.append(f"unresolved reference inventory: expected 145, got {len(refs)}")
    kinds = Counter(ref.get("kind") for ref in refs)
    if dict(kinds) != EXPECTED_UNRESOLVED_KINDS:
        errors.append(f"unresolved kind counts mismatch: {dict(kinds)}")

    for ref in refs:
        target = ref.get("targetLogicalKey", "")
        if target.startswith("domain:"):
            continue
        if target not in documents:
            errors.append(f"unresolved target not present in registry: {target}")

    if action_shape_errors:
        errors.append(f"system.actions must be an object; violations: {action_shape_errors[:5]}")
    if summary.get("status") != "PASS":
        errors.append("step3-summary status is not PASS")

    if errors:
        print("Edgeheart Step 3 source validation FAILED", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("Edgeheart Step 3 source validation PASS")
    print(f" - documents: {len(documents)}")
    print(f" - folders: {len(folders)}")
    print(f" - intentionally unresolved references: {len(refs)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
