# Edgeheart Foundry Build — Step 8 Runtime Qualification Report

**Status:** PASS

## Qualified runtime

- Foundry VTT: **13.351**
- Daggerheart: **1.2.7**
- Edgeheart: **0.1.0**
- Runtime candidate: `edgeheart-v0.1.0.zip`
- Qualified candidate SHA-256:
  `8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

## Manual qualification result

The clean-world runtime candidate was installed and exercised in the frozen
target runtime. User acceptance confirms Step 8 as successful.

Observed checks included:

- every Edgeheart Compendium opened successfully;
- Compendium content appeared correct;
- artwork displayed properly;
- a new Actor was created successfully;
- the Daggerheart Character Builder completed successfully using Edgeheart
  content;
- Edgeheart Domain/Competency SVG glyphs displayed correctly in the Daggerheart
  interface.

These runtime checks supplement, rather than replace, the deterministic source,
asset, reference, and compiled-pack validations from Steps 1–7.

## Acceptance

Step 8 is accepted as **PASS** and the v0.1.0 release gate is cleared.

The exact runtime candidate hash above is the release reproducibility target.
Step 9 must refuse publication if a rebuilt runtime archive differs from the
qualified candidate.
