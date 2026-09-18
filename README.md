# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository intentionally mirrors the successful organizational grammar of
the Cybermancy module while pinning schema/runtime behavior to Daggerheart 1.2.7.

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
tools/          deterministic pack build/extract tooling
```

## Build commands

Install dependencies:

```bash
npm install
```

Validate the module skeleton:

```bash
npm run validate
```

Compile all populated source packs:

```bash
npm run compile:packs
```

Clean and rebuild all Compendia:

```bash
npm run build
```

Extract compiled packs back to JSON source format:

```bash
npm run extract:packs
```

The extraction command requires explicit confirmation before it overwrites JSON
sources.

## Current status

Step 1 — Deployment Contract: accepted and frozen.

Step 2 — Module Skeleton: established.

Step 3 will populate `src/packs/` deterministically from
`edgeheart-consolidated-production-v1.0.zip`.
