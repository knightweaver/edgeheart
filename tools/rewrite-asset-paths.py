#!/usr/bin/env python3
"""Step 6: generate the Edgeheart asset deployment manifest and rewrite source paths.

Edgeheart uses a dual-art contract for its eleven Daggerheart Competencies:
- <domain>.webp: full-color illustration retained as an Edgeheart art asset.
- <domain>.svg: monochrome UI glyph used by Daggerheart's Homebrew Domain src.

Dedicated artwork exists for 538 Foundry source documents. In addition there are
11 Competency illustrations, 11 derived Competency UI glyphs, and 22 adversary
tokens = 582 required deployment assets.

Derived Class/Subclass/Origin Feature documents do not have dedicated artwork
and intentionally retain Daggerheart generic feature art. Embedded
Environment/Adversary features and adversary attack art likewise retain generic
icons.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

MODULE_ID = "edgeheart"

EXPECTED_PRIMARY_COUNTS = {
    "weapon": 64,
    "armor": 25,
    "loot": 40,
    "consumable": 40,
    "cyberware": 60,
    "class": 9,
    "subclass": 18,
    "ancestry": 6,
    "community": 8,
    "domainCard": 231,
    "environment": 15,
    "adversary": 22,
}
EXPECTED_PRIMARY_TOTAL = 538
EXPECTED_COMPETENCY_COUNT = 11
EXPECTED_COMPETENCY_ART_COUNT = 22
EXPECTED_TOKEN_COUNT = 22
EXPECTED_ASSET_TOTAL = 582

DIR_BY_PREFIX = {
    "weapon": "assets/icons/weapons",
    "armor": "assets/icons/armors",
    "loot": "assets/icons/loot",
    "consumable": "assets/icons/consumables",
    "cyberware": "assets/icons/cyberware",
    "class": "assets/icons/classes",
    "subclass": "assets/icons/subclasses",
    "ancestry": "assets/icons/life-paths",
    "community": "assets/icons/affiliations",
    "environment": "assets/icons/environments",
    "adversary": "assets/icons/adversaries",
}

ACTION_ART_PREFIXES = {
    "weapon",
    "armor",
    "loot",
    "consumable",
    "cyberware",
    "domainCard",
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def module_path(repository_path: str) -> str:
    return f"modules/{MODULE_ID}/{repository_path}"

def logical_prefix(key: str) -> str:
    return key.split(":", 1)[0]

def source_slug(doc: dict[str, Any]) -> str:
    slug = (
        doc.get("flags", {})
        .get("edgeheart", {})
        .get("source", {})
        .get("slug")
    )
    if not slug:
        raise ValueError(
            f"{doc.get('name', '<unnamed>')} ({doc.get('_id')}) has no flags.edgeheart.source.slug"
        )
    return slug

def domain_id(doc: dict[str, Any]) -> str:
    domain = doc.get("system", {}).get("domain")
    if not domain:
        raise ValueError(f"{doc.get('name')} domainCard has no system.domain")
    return domain

def primary_repository_path(prefix: str, slug: str, doc: dict[str, Any]) -> str:
    if prefix == "domainCard":
        return f"assets/icons/domains/{domain_id(doc)}/{slug}.webp"
    base = DIR_BY_PREFIX.get(prefix)
    if not base:
        raise ValueError(f"No asset directory mapping for logical prefix: {prefix}")
    return f"{base}/{slug}.webp"

def token_repository_path(slug: str) -> str:
    return f"assets/tokens/adversaries/{slug}-token.png"

def iter_documents(repo: Path):
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
        yield path, key, doc

def rewrite_item_actions(doc: dict[str, Any], art_path: str) -> int:
    rewritten = 0
    attack = doc.get("system", {}).get("attack")
    if isinstance(attack, dict) and "img" in attack:
        if attack.get("img") != art_path:
            attack["img"] = art_path
            rewritten += 1

    actions = doc.get("system", {}).get("actions")
    if actions is not None and not isinstance(actions, dict):
        raise ValueError(f"{doc.get('name')}: system.actions must remain an object")
    if isinstance(actions, dict):
        for action in actions.values():
            if isinstance(action, dict) and "img" in action:
                if action.get("img") != art_path:
                    action["img"] = art_path
                    rewritten += 1
    return rewritten

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    step5 = load_json(repo / "build/step5/step5-summary.json")
    competency_ids = step5.get("competencyIds", [])
    if step5.get("status") != "PASS" or len(competency_ids) != EXPECTED_COMPETENCY_COUNT:
        raise ValueError("Step 5 PASS with exactly 11 Competencies is required")

    entries: list[dict[str, Any]] = []
    primary_counts = Counter()
    nested_images_rewritten = 0
    documents_rewritten = 0
    adversary_slugs: list[str] = []

    for path, key, doc in iter_documents(repo):
        prefix = logical_prefix(key)
        if prefix == "feature":
            continue
        if prefix not in EXPECTED_PRIMARY_COUNTS:
            raise ValueError(f"Unexpected source document logical prefix: {prefix} ({key})")

        slug = source_slug(doc)
        repository_path = primary_repository_path(prefix, slug, doc)
        art_path = module_path(repository_path)

        if doc.get("img") != art_path:
            doc["img"] = art_path
            documents_rewritten += 1

        if prefix in ACTION_ART_PREFIXES:
            nested_images_rewritten += rewrite_item_actions(doc, art_path)

        if prefix == "adversary":
            token_repo = token_repository_path(slug)
            token_path = module_path(token_repo)
            token = doc.get("prototypeToken")
            if not isinstance(token, dict):
                raise ValueError(f"{key}: adversary must have prototypeToken")
            token.setdefault("texture", {})["src"] = token_path
            adversary_slugs.append(slug)
            entries.append({
                "assetId": f"adversaryToken:{slug}",
                "family": "adversary",
                "assetKind": "token",
                "documentLogicalKey": key,
                "sourceFilename": f"{slug}-token.png",
                "repositoryPath": token_repo,
                "modulePath": token_path,
                "required": True,
            })

        dep = (
            doc.setdefault("flags", {})
            .setdefault("edgeheart", {})
            .setdefault("deployment", {})
        )
        dep.update({
            "assetBuildStep": 6,
            "assetPathRewritten": True,
            "primaryAssetPath": art_path,
        })
        if prefix == "adversary":
            dep["tokenAssetPath"] = module_path(token_repository_path(slug))

        path.write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        entries.append({
            "assetId": key,
            "family": prefix,
            "assetKind": "primary",
            "documentLogicalKey": key,
            "sourceFilename": f"{slug}.webp",
            "repositoryPath": repository_path,
            "modulePath": art_path,
            "required": True,
        })
        primary_counts[prefix] += 1

    if dict(primary_counts) != EXPECTED_PRIMARY_COUNTS:
        raise ValueError(
            f"Primary asset counts mismatch: expected {EXPECTED_PRIMARY_COUNTS}, got {dict(primary_counts)}"
        )
    if sum(primary_counts.values()) != EXPECTED_PRIMARY_TOTAL:
        raise ValueError("Primary asset total mismatch")
    if len(adversary_slugs) != EXPECTED_TOKEN_COUNT:
        raise ValueError(f"Expected {EXPECTED_TOKEN_COUNT} adversary tokens")

    # Competencies are native Daggerheart Homebrew Domains, not Compendium
    # documents. Each has both a full illustration and a Daggerheart UI glyph.
    for competency_id in competency_ids:
        illustration_repo = f"assets/icons/domains/{competency_id}.webp"
        glyph_repo = f"assets/icons/domains/{competency_id}.svg"

        entries.append({
            "assetId": f"competency:{competency_id}:illustration",
            "family": "competency",
            "assetKind": "illustration",
            "documentLogicalKey": None,
            "sourceFilename": f"{competency_id}.webp",
            "repositoryPath": illustration_repo,
            "modulePath": module_path(illustration_repo),
            "required": True,
        })
        entries.append({
            "assetId": f"competency:{competency_id}:uiGlyph",
            "family": "competency",
            "assetKind": "uiGlyph",
            "documentLogicalKey": None,
            "sourceFilename": f"{competency_id}.svg",
            "repositoryPath": glyph_repo,
            "modulePath": module_path(glyph_repo),
            "required": True,
        })

    source_names = [entry["sourceFilename"] for entry in entries]
    duplicates = [name for name, count in Counter(source_names).items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate deployment filenames: {duplicates[:10]}")

    entries = sorted(entries, key=lambda e: (e["repositoryPath"], e["assetId"]))

    if len(entries) != EXPECTED_ASSET_TOTAL:
        raise ValueError(
            f"Expected {EXPECTED_ASSET_TOTAL} deployment assets, got {len(entries)}"
        )

    competency_entries = [e for e in entries if e["family"] == "competency"]
    if len(competency_entries) != EXPECTED_COMPETENCY_ART_COUNT:
        raise ValueError("Expected 22 Competency dual-art entries")

    existing = 0
    missing = []
    for entry in entries:
        asset_file = repo / entry["repositoryPath"]
        if asset_file.is_file():
            existing += 1
        else:
            missing.append(entry["repositoryPath"])

    step6 = repo / "build/step6"
    step6.mkdir(parents=True, exist_ok=True)

    dump_json(step6 / "asset-manifest.json", {
        "schemaVersion": "1.1",
        "buildStep": 6,
        "visualCanon": "edgeheart-v0.1.1",
        "domainArtContract": "dual-art-v1",
        "expectedAssetCount": EXPECTED_ASSET_TOTAL,
        "entries": entries,
    })

    summary = {
        "step": 6,
        "status": "PASS" if not missing else "PATHS_REWRITTEN_ASSETS_PENDING",
        "visualCanon": "edgeheart-v0.1.1",
        "domainArtContract": "dual-art-v1",
        "primaryDocumentAssetCount": EXPECTED_PRIMARY_TOTAL,
        "competencyIllustrationAssetCount": EXPECTED_COMPETENCY_COUNT,
        "competencyUiGlyphAssetCount": EXPECTED_COMPETENCY_COUNT,
        "adversaryTokenAssetCount": EXPECTED_TOKEN_COUNT,
        "totalExpectedAssetCount": EXPECTED_ASSET_TOTAL,
        "assetsPresentInRepository": existing,
        "assetsMissingFromRepository": len(missing),
        "documentsWithPrimaryArt": EXPECTED_PRIMARY_TOTAL,
        "nestedActionImagesRewritten": nested_images_rewritten,
        "derivedFeatureArtPolicy": "retain Daggerheart generic feature icons",
        "embeddedActorFeatureArtPolicy": "retain Daggerheart generic feature icons",
        "adversaryAttackArtPolicy": "retain Daggerheart generic attack icon",
        "competencyRuntimeIconPolicy": "Daggerheart Homebrew Domain src uses 250x250 SVG uiGlyph",
        "assetPathsRewritten": True,
        "binaryAssetQualificationPending": bool(missing),
        "compendiumCompilationPending": True,
        "runtimeFoundryQualificationPending": True,
        "nextStep": (
            f"Stage the {len(missing)} missing asset(s) and run "
            "python tools/validate-asset-paths.py --require-assets"
            if missing
            else "Validate staged assets, then compile Foundry Compendia."
        ),
    }
    dump_json(step6 / "step6-summary.json", summary)

    (step6 / "STEP-6-REPORT.md").write_text(
        "# Edgeheart Foundry Build — Step 6 Asset Deployment Report\n\n"
        f"**Status:** {summary['status']}\n\n"
        f"- Source documents with dedicated primary art: **{EXPECTED_PRIMARY_TOTAL}**\n"
        f"- Competency full-color illustrations: **{EXPECTED_COMPETENCY_COUNT}**\n"
        f"- Competency Daggerheart UI SVG glyphs: **{EXPECTED_COMPETENCY_COUNT}**\n"
        f"- Adversary token assets: **{EXPECTED_TOKEN_COUNT}**\n"
        f"- Total required assets: **{EXPECTED_ASSET_TOTAL}**\n"
        f"- Assets currently present in repository: **{existing}**\n"
        f"- Assets still to stage: **{len(missing)}**\n"
        f"- Nested same-document action images rewritten: **{nested_images_rewritten}**\n"
        "- Daggerheart Homebrew Domain src uses the SVG UI glyph, not the full-color WebP.\n"
        "- Derived Feature documents retain generic Daggerheart Feature art.\n"
        "- Embedded Environment/Adversary features retain generic Daggerheart Feature art.\n"
        "- Adversary attack icons remain generic until dedicated attack art exists.\n"
        "- LevelDB Compendium compilation: **pending**\n"
        "- Foundry runtime qualification: **pending**\n",
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
