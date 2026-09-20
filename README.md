# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository mirrors the successful organizational grammar of Cybermancy
while pinning schema/runtime behavior to Daggerheart 1.2.7.

## Runtime

- Foundry VTT 13.351
- Daggerheart 1.2.7

See `DEPLOYMENT-CONTRACT.md` for the frozen implementation contract.

## Release

**Edgeheart v0.1.0 is published and runtime-qualified.**

Release:

https://github.com/knightweaver/edgeheart/releases/tag/v0.1.0

Foundry manifest:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Qualified runtime SHA-256:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

## Pipeline status

Steps 1–9 are complete:

1. deployment contract and module architecture;
2. module skeleton;
3. deterministic source-pack transformation;
4. symbolic reference resolution;
5. native Daggerheart Competency registration;
6. complete 582-asset deployment, including SVG Domain glyphs;
7. compilation and re-extraction validation of all 13 Compendia;
8. clean-world runtime qualification in Foundry 13.351 / Daggerheart 1.2.7;
9. release hardening and publication of v0.1.0.

The published archive is the exact package qualified during Step 8. Fresh release
builds must also match every non-log runtime member and pass all source,
reference, asset, and compiled-pack gates.

## Build authority

- `src/packs/` — editable Foundry source boundary
- `packs/` — generated LevelDB derivative output
- `assets/` — qualified module artwork
- `build/` — validation/report outputs
- `release/` — derivative runtime packages
- `release-control/` — explicit publication requests

Generated packs and runtime ZIPs are not canonical inputs.

## Next

Step 10 — Maintenance and Regression Workflow.
