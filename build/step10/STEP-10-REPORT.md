# Edgeheart Foundry Build — Step 10 Maintenance & Regression Report

**Status:** PASS

## Maintenance authority

Step 10 establishes the released module's routine maintenance system:

- `MAINTENANCE-WORKFLOW.md`
- `maintenance/baseline-v0.1.0.json`
- `maintenance/regression-fixtures-v1.json`
- `maintenance/change-impact-v1.json`
- `maintenance/RUNTIME-SMOKE-TESTS.md`

The v0.1.x baseline freezes the currently qualified corpus at:

- **638** source documents
- **172** structural folders
- **810** source-pack entries
- **582** deployment assets
- **13** compiled Compendia
- Foundry **13.351**
- Daggerheart **1.2.7**

## Named regression fixtures

Eight named fixtures cover the highest-risk integration paths:

1. Runner Class
2. Breach Specialist
3. Net Diver
4. Personal Firewall
5. Military Surplus
6. Corporate Asset
7. Sitil Security Guard
8. Neon Night Market

The suite verifies stable IDs, core document fields, Class/Subclass linkage,
custom Competency Domain behavior, Life Path/Affiliation Feature links,
adversary embedded-Item export keys, token/art paths, and Environment inline
features.

## Change-impact policy

The maintenance classifier now maps changed paths to:

- deterministic validation gates;
- minimum version-bump class;
- targeted versus full clean-world runtime qualification;
- generated-source protections.

A manual direct edit to `src/packs/**` without an accepted source or generator
change is blocking. Controlled GitHub Actions generated-source commits are
allowed but continue through downstream deterministic validation.

Policy regression tests explicitly exercise documentation, art, runtime-code,
canonical-source, module-contract, direct-source, and automated-generated-source
cases.

## Continuous integration

The read-only maintenance workflow completed successfully:

- Workflow run: **35511456620**
- Result: **PASS**

It successfully performed change-impact classification, frozen-baseline and
fixture validation, all source/reference/Competency/asset gates, Compendium
compilation/re-extraction, and runtime-package construction.

The generalized Compendium workflow also completed successfully:

- Workflow run: **35511456605**
- Result: **PASS**

## Future release hardening

The Compendium workflow now derives artifact names and runtime candidate names
from `module.json` rather than hard-coding v0.1.0.

The release workflow now derives release notes, evidence names, archive names,
and other release metadata from the selected version-specific release-control
file. Future releases retain the Step 9 rule: rebuild everything, compare
against the manually qualified candidate, and publish the exact qualified
runtime.

## Version and runtime policy

Step 10 formalizes PATCH / MINOR / MAJOR maintenance rules and two manual runtime
qualification levels:

- targeted smoke test;
- full clean-world qualification.

Intentional v0.1.x corpus-cardinality changes require a reviewed baseline
revision rather than weakening regression checks.

## Acceptance

Step 10 is **PASS**.

Edgeheart now transitions from initial-production development into routine
maintenance mode.
