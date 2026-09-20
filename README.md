# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository mirrors the successful organizational grammar of Cybermancy
while pinning schema/runtime behavior to Daggerheart 1.2.7.

## Runtime

- Foundry VTT 13.351
- Daggerheart 1.2.7

See `DEPLOYMENT-CONTRACT.md` for the frozen implementation contract.

## Repository structure

```text
src/packs/      editable Foundry document sources
packs/          generated LevelDB Compendia (not canonical)
assets/icons/   module artwork by content family
assets/tokens/  VTT token art
scripts/        runtime module code
tools/          deterministic pack build/extract/deployment tooling
sources/        accepted upstream transformation inputs
```

## Current status

Step 1 — Deployment Contract: accepted and frozen; revised to **v1.1** for the
dual-art Competency asset contract.

Step 2 — Module Skeleton: complete.

Step 3 — Deterministic source-pack transformation: complete.

Step 4 — Symbolic reference and class Competency mapping resolution: complete.

Step 5 — Native Competency registration: complete. Homebrew Domain `src` now
uses the Daggerheart-compatible SVG UI glyph, with safe migration from the
previous Edgeheart WebP path.

Step 6 — Asset deployment: **571 raster assets are staged; 11 derived SVG
Competency UI glyphs remain to generate and stage**. The final required asset
count is **582**.

Each Competency now has:

```text
assets/icons/domains/<domain>.webp   # full Edgeheart illustration
assets/icons/domains/<domain>.svg    # Daggerheart UI glyph
```

Competency Cards continue to use:

```text
assets/icons/domains/<domain>/<card-slug>.webp
```

See `ASSET-STAGING.md` for the complete staging and SVG validation contract.

## Relevant commands

```bash
npm run validate:competencies
npm run rewrite:assets
npm run validate:asset-paths
npm run validate:assets
```

Compendium compilation and clean-world Foundry runtime qualification remain
downstream of final 582-asset validation.
