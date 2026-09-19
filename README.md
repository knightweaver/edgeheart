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
sources/        accepted upstream transformation inputs
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

Step 3 — Deterministic source-pack transformation: complete and authoritative in
GitHub.

Step 4 — Symbolic reference and class Competency mapping resolution: complete
and authoritative in GitHub.

Step 5 — Native Competency registration: **complete and authoritative in
GitHub**. Edgeheart now registers Network, Assault, Chrome, Systems, Influence,
Ghost, Frontier, Medtech, Aegis, Redline, and Blackwall through Daggerheart
1.2.7's native world-scoped Homebrew domain setting. Static validation confirms
all 231 Domain Cards use those IDs, 21 cards per Competency, and all 9 class
mappings are valid.

To regenerate and validate Steps 3–5 locally:

```bash
npm run build:sources -- /path/to/edgeheart-consolidated-production-v1.0.zip
npm run validate:sources
npm run resolve:references
npm run validate:references
npm run validate:competencies
```

The accepted source archive remains:

`sources/edgeheart-consolidated-production-v1.0.zip`

The next deployment work is final asset staging and deterministic asset-path
rewriting, followed by Compendium compilation and clean-world Foundry runtime
qualification.
