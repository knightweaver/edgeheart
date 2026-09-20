# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository mirrors the successful organizational grammar of Cybermancy
while pinning schema/runtime behavior to Daggerheart 1.2.7.

## Runtime

- Foundry VTT 13.351
- Daggerheart 1.2.7

See `DEPLOYMENT-CONTRACT.md` for the frozen implementation contract.

## Current status

Steps 1–7 are complete and authoritative in GitHub:

1. deployment contract and module architecture;
2. module skeleton;
3. deterministic source-pack transformation;
4. symbolic reference resolution;
5. native Daggerheart Competency registration;
6. complete 582-asset deployment, including approved SVG Domain glyphs;
7. deterministic compilation and re-extraction validation of all 13 Compendia.

Step 7 validates **810 / 810** source/compiled pack entries. A deterministic
Edgeheart 0.1.0 runtime candidate has also been built with SHA-256:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

The next gate is **Step 8 — clean-world runtime qualification** against exactly
Foundry 13.351 and Daggerheart 1.2.7. See `RUNTIME-QUALIFICATION.md`.

## Build authority

- `src/packs/` — editable Foundry source boundary
- `packs/` — generated LevelDB derivative output
- `assets/` — qualified module artwork
- `build/` — validation/report outputs
- `release/` — derivative runtime packages

Generated packs and runtime ZIPs are not canonical inputs.
