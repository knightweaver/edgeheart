# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository mirrors the successful organizational grammar of Cybermancy
while pinning schema/runtime behavior to Daggerheart 1.2.7.

## Runtime

- Foundry VTT 13.351
- Daggerheart 1.2.7

## Current release

**Edgeheart v0.1.0 is published and runtime-qualified.**

Release:

https://github.com/knightweaver/edgeheart/releases/tag/v0.1.0

Foundry manifest:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Qualified runtime SHA-256:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

## Pipeline status

Steps 1–10 are complete:

1. deployment contract and module architecture;
2. module skeleton;
3. deterministic source-pack transformation;
4. symbolic reference resolution;
5. native Daggerheart Competency registration;
6. complete 582-asset deployment, including SVG Domain glyphs;
7. compilation and re-extraction validation of all 13 Compendia;
8. clean-world runtime qualification;
9. release hardening and publication of v0.1.0;
10. maintenance, regression, change-impact, versioning, and future-release workflow.

Edgeheart is now in **routine maintenance mode**.

## Maintenance

The authoritative procedure is:

`MAINTENANCE-WORKFLOW.md`

Useful commands:

```powershell
npm run validate:regressions
npm run validate:policy
npm run validate:maintenance
npm run build:maintenance
```

Change impact can be classified with:

```powershell
python tools\maintenance-status.py --paths <changed-paths>
```

The v0.1.x maintenance baseline freezes the currently qualified 638 documents,
172 structural folders, 810 pack entries, 582 assets, and 13 Compendia.
Intentional corpus changes require a reviewed versioned baseline update.

## Build authority

- `sources/` — accepted upstream source package
- `src/packs/` — deterministic Foundry source boundary
- `assets/` — qualified module artwork
- `packs/` — generated LevelDB derivative output
- `maintenance/` — baseline, regression, and impact policy
- `build/` — validation/report outputs
- `release/` — derivative runtime packages
- `release-control/` — explicit publication requests

Generated packs and runtime ZIPs are not canonical inputs.
