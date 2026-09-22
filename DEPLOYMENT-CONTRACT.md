# Edgeheart Foundry Deployment Contract v1.2

**Status:** FROZEN / FINAL LEGACY RELEASE CONTRACT

v1.2 supersedes v1.1 only for release compatibility metadata. The content,
schema mappings, stable IDs, Compendia, assets, and runtime implementation remain
those qualified in v0.1.0.

## Runtime authority and declared support

The implementation was built and manually qualified on:

- Foundry VTT **13.351**
- Daggerheart **1.2.7**

The final legacy-series manifest intentionally broadens package compatibility to:

- Foundry VTT **13.x** — `minimum: 13`, `verified: 13`, `maximum: 13`
- Daggerheart **1.2.x** — `minimum: 1.2`, `verified: 1.2`, no hard maximum

The Daggerheart maximum is intentionally omitted. Foundry package version
comparison treats a patch version such as 1.2.7 as newer than the shorter
version 1.2; setting `maximum: 1.2` would therefore risk blocking the exact
1.2.7 runtime that Edgeheart was qualified against.

This release does **not** claim compatibility with Foundry 14 or Daggerheart
2.x. Those are a separate migration target.

- Edgeheart module id: **`edgeheart`**
- Repository: **`knightweaver/edgeheart`**

## Canonical inputs

- `edgeheart-consolidated-production-v1.0.zip`
- accepted Edgeheart Visual Canon **v0.1.1**
- generated Edgeheart art assets produced from the accepted art manifest
- derived Competency SVG UI glyphs produced from the accepted Competency artwork

The neutral Edgeheart corpus remains the source-content authority. Foundry JSON,
compiled Compendia, release ZIPs, and rendered art are derivative outputs.

## Module organization

- editable pack sources under `src/packs/`
- compiled Foundry LevelDB packs under `packs/`
- module art under `assets/icons/`
- adversary tokens under `assets/tokens/adversaries/`
- Compendium groups: `Items`, `System`, `Adventures`

## Compendia

### Items
- Weapons
- Armors
- Loot
- Consumables
- Cyberware

### System
- Classes
- Subclasses
- Competencies
- Features
- Life Paths
- Affiliations

### Adventures
- Adversaries
- Environments

Daggerheart-native document types remain authoritative internally:

- Life Paths -> `ancestry`
- Affiliations -> `community`
- Competency Cards -> `domainCard`

## Domain / Competency extension

Do not patch Daggerheart.

The eleven Edgeheart Competencies use the Daggerheart 1.2 Homebrew Domain
mechanism and are exposed through `CONFIG.DH.DOMAIN.allDomains()`.

Each Competency has:

1. full-color illustration: `assets/icons/domains/<domain>.webp`
2. monochrome UI glyph: `assets/icons/domains/<domain>.svg`

The SVG is the runtime interface icon.

## Asset path contract

All module assets use portable `modules/edgeheart/...` paths, never
world-specific paths.

The complete deployment contains **582 required assets**:
538 document primary images + 11 Competency illustrations + 11 Competency SVG
glyphs + 22 adversary tokens.

## Build authority

`src/packs/` is the deterministic Foundry source boundary.

`packs/` is generated LevelDB output and must be reproducible from
`src/packs/` using `@foundryvtt/foundryvtt-cli`.

Bundle symbolic references must be resolved to stable Edgeheart Compendium UUIDs
before compilation.
