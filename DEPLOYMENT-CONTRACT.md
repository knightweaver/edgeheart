# Edgeheart Foundry Deployment Contract v1.0

**Status:** FROZEN / ACCEPTED

## Runtime target

- Foundry VTT: **13.351**
- Daggerheart system: **1.2.7**
- Edgeheart module id: **`edgeheart`**
- Intended repository: **`knightweaver/edgeheart`**

Implementation and schema decisions are pinned to the Daggerheart `1.2.7` tag.
Later Daggerheart releases are not authoritative for this build.

## Canonical inputs

- `edgeheart-consolidated-production-v1.0.zip`
- accepted Edgeheart Visual Canon **v0.1.1**
- generated Edgeheart art assets produced from the accepted art manifest

The neutral Edgeheart corpus remains the source-content authority. Foundry JSON,
compiled Compendia, release ZIPs, and rendered art are derivative outputs.

## Module organization

Mirror the established Cybermancy module grammar wherever applicable:

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

Do not patch the Daggerheart installation.

The eleven Edgeheart Competencies will be registered through Daggerheart 1.2.7's
native Homebrew domain setting and exposed through `CONFIG.DH.DOMAIN.allDomains()`.

## Asset path contract

All module assets use portable module paths, never world-specific paths.

Examples:

- `modules/edgeheart/assets/icons/weapons/<slug>.webp`
- `modules/edgeheart/assets/icons/armors/<slug>.webp`
- `modules/edgeheart/assets/icons/loot/<slug>.webp`
- `modules/edgeheart/assets/icons/consumables/<slug>.webp`
- `modules/edgeheart/assets/icons/cyberware/<slug>.webp`
- `modules/edgeheart/assets/icons/classes/<slug>.webp`
- `modules/edgeheart/assets/icons/subclasses/<slug>.webp`
- `modules/edgeheart/assets/icons/life-paths/<slug>.webp`
- `modules/edgeheart/assets/icons/affiliations/<slug>.webp`
- `modules/edgeheart/assets/icons/environments/<slug>.webp`
- `modules/edgeheart/assets/icons/adversaries/<slug>.webp`
- `modules/edgeheart/assets/icons/domains/<domain>.webp`
- `modules/edgeheart/assets/icons/domains/<domain>/<card-slug>.webp`
- `modules/edgeheart/assets/tokens/adversaries/<slug>-token.png`

## Build authority

`src/packs/` is the editable Foundry source boundary.

`packs/` is generated LevelDB output and must be reproducible from `src/packs/`
using `@foundryvtt/foundryvtt-cli`.

Bundle symbolic references must be resolved to stable Edgeheart Compendium UUIDs
before pack compilation.
