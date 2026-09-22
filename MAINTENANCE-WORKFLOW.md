# Edgeheart Maintenance Workflow

## Authority

This is the authoritative routine-maintenance workflow for the released
Edgeheart module. The final legacy release declares support for Foundry **13.x** and Daggerheart **1.2.x**. The implementation was originally runtime-qualified on Foundry **13.351** / Daggerheart **1.2.7**. Foundry 14 / Daggerheart 2.x is a separate migration target.

Authority flows:

```text
accepted consolidated source package
-> deterministic source-pack build
-> resolved src/packs sources
-> qualified assets
-> compiled LevelDB derivative packs
-> runtime candidate
-> required Foundry qualification
-> release
```

Never promote generated LevelDB, runtime ZIPs, or unexplained hand edits over
their upstream authority.

## Status and change impact

For intended paths:

```powershell
python tools\maintenance-status.py --paths <path-1> <path-2>
```

For committed changes:

```powershell
python tools\maintenance-status.py --base <base-commit> --head HEAD
```

The report identifies required automated gates, minimum version-bump class,
runtime qualification level, and prohibited direct edits to generated
`src/packs`.

## Canonical content changes

For an intentional content correction or corpus change:

1. update the accepted consolidated source package/provenance;
2. update the deployment contract and maintenance baseline if source version,
   runtime contract, or corpus cardinality changes;
3. regenerate and validate:
   ```powershell
   npm run build:sources -- sources\<accepted-package>.zip
   npm run validate:sources
   npm run resolve:references
   npm run validate:references
   npm run validate:competencies
   npm run rewrite:assets
   npm run validate:assets
   npm run validate:regressions
   ```
4. review generated `src/packs/`;
5. run:
   ```powershell
   npm run clean:packs
   npm run compile:packs
   npm run validate:compiled-packs
   npm run build:runtime-package
   ```
6. perform the runtime qualification required by the impact policy.

Direct hand-editing `src/packs` without an accepted source/generator change is
blocked by maintenance policy.

## Art changes

For artwork replacement at the same logical path:

```powershell
npm run validate:assets
npm run validate:regressions
npm run build:runtime-package
```

Then perform a targeted Foundry smoke test of the affected document or UI.
Path-contract, Domain-glyph, or staging-rule changes are tooling/runtime changes
and require the larger gate set.

## Runtime/Competency changes

Changes to `scripts/`, native Homebrew Domain registration, module startup, or
Daggerheart integration require all automated gates plus a **full clean-world
runtime qualification**. Never patch Daggerheart itself.

## Regression authority

Baseline:

`maintenance/baseline-v0.1.1.json`

Fixtures:

`maintenance/regression-fixtures-v1.json`

The fixtures deliberately exercise Runner/Class/Subclass references, a Network
Domain Card, Life Path/Affiliation feature links, an adversary with embedded
Features/token art, and an Environment with inline Features.

Run:

```powershell
npm run validate:regressions
```

The v0.1.x counts are frozen regression expectations. Intentional entity
additions/removals require a reviewed baseline revision and normally a MINOR
version bump; do not weaken the test to accommodate accidental drift.

## Continuous integration

`.github/workflows/maintenance-regression.yml` is read-only. It classifies
change impact, validates baseline/fixtures, reruns source/reference/Competency/
asset gates, compiles and re-extracts all Compendia, and builds a runtime
candidate. It uploads evidence and never publishes a release.

## Versioning

- **PATCH** — correction preserving exposed roster, stable Compendium identity,
  and runtime contract.
- **MINOR** — backward-compatible content/feature expansion or intentional
  corpus-cardinality change.
- **MAJOR** — breaking module ID, Compendium UUID/name contract, runtime target,
  or incompatible schema/deployment change.

While pre-1.0, a deliberate breaking change may use a 0.x minor bump only when
explicitly labeled breaking and given full clean-world qualification.

`module.json` and `package.json` versions must match at release.

## Runtime qualification

**Targeted smoke:** ordinary patch changes with no schema/runtime change. Install
the candidate, enable Edgeheart, exercise the changed pack/entity/UI, verify art,
and inspect the console.

**Full clean-world:** canonical corpus changes, runtime code, Competency
registration, Class/Subclass/Origin/reference contracts, module/Compendium
contracts, runtime target changes, and breaking changes. Repeat Step 8 including
Character Builder and SVG Domain verification.

See `maintenance/RUNTIME-SMOKE-TESTS.md`.

## Release checkpoint

A release requires:

1. automated maintenance gates PASS;
2. required runtime qualification PASS;
3. matching version in `module.json` and `package.json`;
4. `RELEASE-NOTES-vX.Y.Z.md`;
5. the qualified runtime candidate retained as an Actions artifact;
6. `release-control/vX.Y.Z.json` containing its workflow run, artifact name,
   and exact SHA-256;
7. commit/push of the release-control file.

The release workflow rebuilds from source and publishes the **exact qualified
candidate** only after equivalence checks. LevelDB `LOG` and `LOG.old` may
vary; no other runtime member may differ.

Do not release every maintenance commit. Publish coherent user-visible fixes,
content updates, installed-behavior changes, or compatibility/security fixes.
Documentation/developer-only changes may accumulate without a release.

## Current legacy baseline

Edgeheart v0.1.1:

- 638 source documents
- 172 structural folders
- 810 pack entries
- 582 assets
- 13 Compendia
- declared support: Foundry 13.x / Daggerheart 1.2.x
- original runtime qualification: Foundry 13.351 / Daggerheart 1.2.7
- runtime SHA-256
  `8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`
