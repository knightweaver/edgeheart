#!/usr/bin/env python3
"""Repair Foundry embedded-document _key metadata for Edgeheart Actor sources.

Foundry's LevelDB compiler requires exported embedded Actor Items/Effects to
carry their canonical hierarchical _key values. The upstream Edgeheart direct
Actor payloads include stable embedded _id values but omit these export keys.

This tool adds only deterministic Foundry export metadata; it does not alter
game mechanics, names, descriptions, or stable IDs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ACTOR_PACKS = (
    "src/packs/adventures/adversaries",
    "src/packs/adventures/environments",
)

def repair_actor(doc: dict) -> tuple[int, int, int]:
    actor_id = doc.get("_id")
    if not actor_id:
        raise ValueError(f"Actor {doc.get('name','<unnamed>')} is missing _id")

    item_updates = 0
    item_effect_updates = 0
    actor_effect_updates = 0

    for item in doc.get("items", []) or []:
        item_id = item.get("_id")
        if not item_id:
            raise ValueError(
                f"Actor {doc.get('name')} embedded Item {item.get('name')} is missing _id"
            )
        expected = f"!actors.items!{actor_id}.{item_id}"
        if item.get("_key") != expected:
            item["_key"] = expected
            item_updates += 1

        for effect in item.get("effects", []) or []:
            effect_id = effect.get("_id")
            if not effect_id:
                raise ValueError(
                    f"Actor {doc.get('name')} Item {item.get('name')} effect is missing _id"
                )
            expected_effect = (
                f"!actors.items.effects!{actor_id}.{item_id}.{effect_id}"
            )
            if effect.get("_key") != expected_effect:
                effect["_key"] = expected_effect
                item_effect_updates += 1

    for effect in doc.get("effects", []) or []:
        effect_id = effect.get("_id")
        if not effect_id:
            raise ValueError(f"Actor {doc.get('name')} effect is missing _id")
        expected_effect = f"!actors.effects!{actor_id}.{effect_id}"
        if effect.get("_key") != expected_effect:
            effect["_key"] = expected_effect
            actor_effect_updates += 1

    return item_updates, item_effect_updates, actor_effect_updates

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    actor_count = 0
    changed_files = 0
    items = item_effects = actor_effects = 0

    for rel in ACTOR_PACKS:
        pack = repo / rel
        for path in sorted(pack.glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            if str(doc.get("_key", "")).startswith("!folders!"):
                continue
            if doc.get("type") not in ("adversary", "environment"):
                continue

            actor_count += 1
            before = json.dumps(doc, sort_keys=True)
            a, b, c = repair_actor(doc)
            items += a
            item_effects += b
            actor_effects += c

            if json.dumps(doc, sort_keys=True) != before:
                path.write_text(
                    json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                changed_files += 1

    print(f"Actors inspected: {actor_count}")
    print(f"Source files changed: {changed_files}")
    print(f"Embedded Item _keys added/repaired: {items}")
    print(f"Embedded Item Effect _keys added/repaired: {item_effects}")
    print(f"Embedded Actor Effect _keys added/repaired: {actor_effects}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
