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

Step 5 — Native Competency registration: complete. Homebrew Domain `src` uses
the Daggerheart-compatible SVG UI glyph, with safe migration from the previous
Edgeheart WebP path.

Step 6 — Asset deployment: **complete**.

The repository now contains the complete qualified **582-asset** deployment:

- 538 source-document primary images
- 11 full-color Competency WebP illustrations
- 11 approved Competency SVG UI glyphs
- 22 adversary token PNGs

All 582 assets passed the deterministic asset qualification workflow.

Each Competency has:

```text
assets/icons/domains/<domain>.webp   # full Edgeheart illustration
assets/icons/domains/<domain>.svg    # Daggerheart UI glyph
```

Competency Cards continue to use:

```text
assets/icons/domains/<domain>/<card-slug>.webp
```

See `ASSET-STAGING.md` and `STEP-6-HANDOFF.md` for the complete asset
contract and qualification record.

## Relevant commands

```bash
npm run validate:competencies
npm run rewrite:assets
npm run generate:glyphs
npm run validate:asset-paths
npm run validate:assets
```

The next build unit is deterministic Compendium compilation from
`src/packs/`, followed by compiled-pack validation and clean-world Foundry
runtime qualification.
