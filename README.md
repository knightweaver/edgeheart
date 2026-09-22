# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

## Legacy runtime line

**Edgeheart v0.1.1** is the final release before migration to Foundry 14 /
Daggerheart 2.x.

Declared support:

- Foundry VTT **13.x**
- Daggerheart **1.2.x**

The implementation was originally fully runtime-qualified on Foundry 13.351 /
Daggerheart 1.2.7. v0.1.1 changes compatibility metadata only; its Edgeheart
content, runtime scripts, stable IDs, assets, and Compendium structure are
unchanged from v0.1.0.

Install/update manifest:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Tagged prior releases can be addressed directly through their GitHub release
URLs.

## Pipeline status

Steps 1–10 are complete. The legacy line is in maintenance/frozen state while
the next development phase migrates Edgeheart to Foundry 14 / Daggerheart 2.x.

## Maintenance

See:

- `DEPLOYMENT-CONTRACT.md`
- `MAINTENANCE-WORKFLOW.md`
- `LEGACY-RUNTIME-NOTES.md`
- `maintenance/baseline-v0.1.1.json`

Useful commands:

```powershell
npm run validate:regressions
npm run validate:policy
npm run validate:maintenance
npm run build:maintenance
```

## Build authority

- `sources/` — accepted upstream source package
- `src/packs/` — deterministic Foundry source boundary
- `assets/` — qualified module artwork
- `packs/` — generated LevelDB derivative output
- `maintenance/` — baseline, regression, and impact policy
- `build/` — validation/report outputs
- `release/` — derivative runtime packages
- `release-control/` — explicit publication requests
