#!/usr/bin/env python3
"""Validate Edgeheart Step 6 asset-path rewriting and optional staged binaries."""
from __future__ import annotations

import argparse
import json
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any

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
EXPECTED_ASSET_TOTAL = 571
EXPECTED_COMPETENCIES = 11
EXPECTED_TOKENS = 22

ACTION_ART_PREFIXES = {
    "weapon",
    "armor",
    "loot",
    "consumable",
    "cyberware",
    "domainCard",
}

EXPECTED_SIZE_BY_FAMILY_KIND = {
    ("weapon", "primary"): (1024, 1024),
    ("armor", "primary"): (1024, 1024),
    ("loot", "primary"): (1024, 1024),
    ("consumable", "primary"): (1024, 1024),
    ("cyberware", "primary"): (1024, 1024),
    ("class", "primary"): (1024, 1280),
    ("subclass", "primary"): (1024, 1280),
    ("ancestry", "primary"): (1024, 1280),
    ("community", "primary"): (1024, 1280),
    ("competency", "primary"): (1024, 1024),
    ("domainCard", "primary"): (1024, 1024),
    ("environment", "primary"): (1536, 1024),
    ("adversary", "primary"): (1024, 1280),
    ("adversary", "token"): (1024, 1024),
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def logical_prefix(key: str) -> str:
    return key.split(":", 1)[0]

def png_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
        raise ValueError("invalid PNG signature")
    return struct.unpack(">II", data[16:24])

def png_has_alpha(data: bytes) -> bool:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 29:
        return False
    color_type = data[25]
    if color_type in (4, 6):
        return True
    return b"tRNS" in data

def webp_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 20 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("invalid WebP signature")
    offset = 12
    while offset + 8 <= len(data):
        fourcc = data[offset:offset + 4]
        size = int.from_bytes(data[offset + 4:offset + 8], "little")
        payload = data[offset + 8:offset + 8 + size]
        if fourcc == b"VP8X" and len(payload) >= 10:
            width = 1 + int.from_bytes(payload[4:7], "little")
            height = 1 + int.from_bytes(payload[7:10], "little")
            return width, height
        if fourcc == b"VP8 " and len(payload) >= 10:
            if payload[3:6] != b"\x9d\x01\x2a":
                raise ValueError("invalid VP8 frame header")
            width = int.from_bytes(payload[6:8], "little") & 0x3FFF
            height = int.from_bytes(payload[8:10], "little") & 0x3FFF
            return width, height
        if fourcc == b"VP8L" and len(payload) >= 5:
            if payload[0] != 0x2F:
                raise ValueError("invalid VP8L signature")
            bits = int.from_bytes(payload[1:5], "little")
            width = 1 + (bits & 0x3FFF)
            height = 1 + ((bits >> 14) & 0x3FFF)
            return width, height
        offset += 8 + size + (size & 1)
    raise ValueError("could not determine WebP dimensions")

def image_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if path.suffix.lower() == ".png":
        return png_dimensions(data)
    if path.suffix.lower() == ".webp":
        return webp_dimensions(data)
    raise ValueError(f"unsupported asset extension: {path.suffix}")

def document_index(repo: Path):
    docs = {}
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
            raise ValueError(f"Missing logicalKey: {path.relative_to(repo)}")
        docs[key] = (path, doc)
    return docs

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--require-assets",
        action="store_true",
        help="Require all 571 staged image binaries and validate format/dimensions."
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors: list[str] = []

    manifest_path = repo / "build/step6/asset-manifest.json"
    summary_path = repo / "build/step6/step6-summary.json"
    if not manifest_path.is_file():
        errors.append("missing build/step6/asset-manifest.json")
    if not summary_path.is_file():
        errors.append("missing build/step6/step6-summary.json")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    manifest = load_json(manifest_path)
    entries = manifest.get("entries", [])
    if manifest.get("expectedAssetCount") != EXPECTED_ASSET_TOTAL:
        errors.append("asset manifest expectedAssetCount must be 571")
    if len(entries) != EXPECTED_ASSET_TOTAL:
        errors.append(f"asset manifest must contain 571 entries, got {len(entries)}")

    # Manifest identity and path checks.
    repository_paths = [e.get("repositoryPath") for e in entries]
    module_paths = [e.get("modulePath") for e in entries]
    source_filenames = [e.get("sourceFilename") for e in entries]
    for label, values in (
        ("repositoryPath", repository_paths),
        ("modulePath", module_paths),
        ("sourceFilename", source_filenames),
    ):
        if len(values) != len(set(values)):
            errors.append(f"duplicate {label} values in asset manifest")

    for entry in entries:
        repo_path = entry["repositoryPath"]
        expected_module = f"modules/edgeheart/{repo_path}"
        if entry["modulePath"] != expected_module:
            errors.append(
                f"{entry['assetId']}: modulePath {entry['modulePath']} != {expected_module}"
            )
        if repo_path.startswith("/") or ".." in Path(repo_path).parts:
            errors.append(f"{entry['assetId']}: nonportable repositoryPath {repo_path}")

    docs = document_index(repo)
    if len(docs) != 638:
        errors.append(f"expected 638 Foundry source documents, got {len(docs)}")

    primary_counts = Counter()
    primary_by_key = {
        e["documentLogicalKey"]: e
        for e in entries
        if e.get("assetKind") == "primary" and e.get("documentLogicalKey")
    }
    token_by_key = {
        e["documentLogicalKey"]: e
        for e in entries
        if e.get("assetKind") == "token"
    }

    derived_features = 0
    for key, (path, doc) in docs.items():
        prefix = logical_prefix(key)
        dep = doc.get("flags", {}).get("edgeheart", {}).get("deployment", {})

        if prefix == "feature":
            derived_features += 1
            if doc.get("img") != "icons/svg/aura.svg":
                errors.append(
                    f"{path.relative_to(repo)}: derived Feature should retain icons/svg/aura.svg"
                )
            actions = doc.get("system", {}).get("actions")
            if actions is not None and not isinstance(actions, dict):
                errors.append(f"{path.relative_to(repo)}: system.actions must remain an object")
            if isinstance(actions, dict):
                for action in actions.values():
                    if isinstance(action, dict) and "img" in action:
                        if action["img"] != "icons/svg/aura.svg":
                            errors.append(
                                f"{path.relative_to(repo)}: derived Feature action should retain generic aura art"
                            )
            continue

        entry = primary_by_key.get(key)
        if not entry:
            errors.append(f"{path.relative_to(repo)}: no primary asset-manifest entry")
            continue

        expected = entry["modulePath"]
        if doc.get("img") != expected:
            errors.append(
                f"{path.relative_to(repo)}: img {doc.get('img')} != {expected}"
            )
        if not dep.get("assetPathRewritten") or dep.get("assetBuildStep") != 6:
            errors.append(f"{path.relative_to(repo)}: missing Step 6 deployment flags")
        if dep.get("primaryAssetPath") != expected:
            errors.append(f"{path.relative_to(repo)}: primaryAssetPath mismatch")

        if prefix in ACTION_ART_PREFIXES:
            attack = doc.get("system", {}).get("attack")
            if isinstance(attack, dict) and "img" in attack and attack["img"] != expected:
                errors.append(
                    f"{path.relative_to(repo)}: system.attack.img must reuse primary art"
                )
            actions = doc.get("system", {}).get("actions")
            if actions is not None and not isinstance(actions, dict):
                errors.append(f"{path.relative_to(repo)}: system.actions must remain an object")
            if isinstance(actions, dict):
                for action in actions.values():
                    if isinstance(action, dict) and "img" in action:
                        if action["img"] != expected:
                            errors.append(
                                f"{path.relative_to(repo)}: same-document action img must reuse primary art"
                            )

        if prefix == "adversary":
            token_entry = token_by_key.get(key)
            if not token_entry:
                errors.append(f"{path.relative_to(repo)}: no adversary token manifest entry")
            else:
                actual = doc.get("prototypeToken", {}).get("texture", {}).get("src")
                if actual != token_entry["modulePath"]:
                    errors.append(
                        f"{path.relative_to(repo)}: prototypeToken.texture.src mismatch"
                    )
                if dep.get("tokenAssetPath") != token_entry["modulePath"]:
                    errors.append(f"{path.relative_to(repo)}: tokenAssetPath mismatch")
            attack_img = doc.get("system", {}).get("attack", {}).get("img")
            if attack_img and attack_img.startswith("modules/edgeheart/"):
                errors.append(
                    f"{path.relative_to(repo)}: adversary attack art should remain generic"
                )
            for item in doc.get("items", []):
                if str(item.get("img", "")).startswith("modules/edgeheart/"):
                    errors.append(
                        f"{path.relative_to(repo)}: embedded adversary Feature art should remain generic"
                    )

        if prefix == "environment":
            for feature in doc.get("system", {}).get("features", []):
                if str(feature.get("img", "")).startswith("modules/edgeheart/"):
                    errors.append(
                        f"{path.relative_to(repo)}: embedded Environment Feature art should remain generic"
                    )

        primary_counts[prefix] += 1

    if derived_features != 100:
        errors.append(f"expected 100 derived Feature docs, got {derived_features}")
    if dict(primary_counts) != EXPECTED_PRIMARY_COUNTS:
        errors.append(
            f"primary document counts mismatch: expected {EXPECTED_PRIMARY_COUNTS}, got {dict(primary_counts)}"
        )
    if sum(primary_counts.values()) != EXPECTED_PRIMARY_TOTAL:
        errors.append("expected 538 source documents with dedicated primary art")

    competency_entries = [
        e for e in entries
        if e.get("family") == "competency" and e.get("assetKind") == "primary"
    ]
    token_entries = [e for e in entries if e.get("assetKind") == "token"]
    if len(competency_entries) != EXPECTED_COMPETENCIES:
        errors.append(f"expected 11 Competency asset entries, got {len(competency_entries)}")
    if len(token_entries) != EXPECTED_TOKENS:
        errors.append(f"expected 22 adversary token entries, got {len(token_entries)}")

    competency_source = (repo / "scripts/competencies.js").read_text(encoding="utf-8")
    for entry in competency_entries:
        if entry["modulePath"] not in competency_source:
            errors.append(
                f"{entry['assetId']}: Competency registration does not reference {entry['modulePath']}"
            )

    # Binary validation is intentionally optional until the locally generated
    # artwork has been staged into the repository.
    existing = 0
    missing = []
    binary_errors = []
    for entry in entries:
        asset_path = repo / entry["repositoryPath"]
        if not asset_path.is_file():
            missing.append(entry["repositoryPath"])
            continue
        existing += 1
        if not args.require_assets:
            continue
        try:
            actual_size = image_dimensions(asset_path)
            expected_size = EXPECTED_SIZE_BY_FAMILY_KIND[
                (entry["family"], entry["assetKind"])
            ]
            if actual_size != expected_size:
                binary_errors.append(
                    f"{entry['repositoryPath']}: expected {expected_size[0]}x{expected_size[1]}, "
                    f"got {actual_size[0]}x{actual_size[1]}"
                )
            if entry["assetKind"] == "token":
                data = asset_path.read_bytes()
                if not png_has_alpha(data):
                    binary_errors.append(
                        f"{entry['repositoryPath']}: adversary token PNG must support transparency"
                    )
        except Exception as exc:
            binary_errors.append(f"{entry['repositoryPath']}: {exc}")

    if args.require_assets and missing:
        errors.append(f"{len(missing)} required assets are missing")
    if binary_errors:
        errors.extend(binary_errors)

    if errors:
        print("Edgeheart Step 6 asset validation FAILED", file=sys.stderr)
        for error in errors[:100]:
            print(f" - {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f" - ... {len(errors) - 100} additional error(s)", file=sys.stderr)
        return 1

    print("Edgeheart Step 6 asset-path validation PASS")
    print(" - dedicated primary document art paths: 538")
    print(" - Competency icon paths: 11")
    print(" - adversary token paths: 22")
    print(" - total deployment assets: 571")
    print(f" - asset binaries currently present: {existing}")
    print(f" - asset binaries currently missing: {len(missing)}")
    if args.require_assets:
        print(" - image formats/dimensions/transparency: PASS")
    else:
        print(" - binary presence qualification: deferred (use --require-assets)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
