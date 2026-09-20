# Step 10 Handoff — Maintenance & Regression Workflow

## Status

**COMPLETE / AUTHORITATIVE IN GITHUB**

Edgeheart now has a permanent maintenance and regression system for changes
after the qualified v0.1.0 release.

## Routine commands

Read-only regression validation:

```powershell
npm run validate:regressions
npm run validate:policy
npm run validate:maintenance
```

Full local derivative build:

```powershell
npm run build:maintenance
```

Change-impact assessment:

```powershell
python tools\maintenance-status.py --paths <changed-paths>
```

or:

```powershell
python tools\maintenance-status.py --base <base-commit> --head HEAD
```

## Governance

- v0.1.x corpus counts are frozen in `maintenance/baseline-v0.1.0.json`.
- stable regression exemplars are in
  `maintenance/regression-fixtures-v1.json`.
- direct unexplained `src/packs` edits are blocked.
- generated-source bot commits are accepted only alongside downstream
  deterministic validation.
- runtime qualification requirements are determined by change impact.
- release publication remains explicit through versioned release-control files.

## Validated CI

Maintenance regression workflow **35511456620**: PASS.

Generalized Compendium build workflow **35511456605**: PASS.

## Project state

Steps 1–10 are complete. Edgeheart is now in routine maintenance mode rather
than an unfinished production pipeline.
