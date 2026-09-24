# Edgeheart v0.2.0 — Foundry 14 / Daggerheart 2

This release migrates Edgeheart's Compendia for Foundry VTT 14 and the
Daggerheart 2 system. The exact runtime qualification target is Foundry
**14.368** with Daggerheart **2.10.5**.

## Content migration

- All 13 Compendia retain their 638 logical documents, 172 folders, and 582
  artwork assets. Existing document IDs and subclass links are preserved.
- Environment Actors now contain their 49 Features as embedded Items. Impulses
  and potential adversary fields use the Daggerheart 2 data shape. Matching
  Edgeheart adversaries link to their Compendium Actors; Cordon Eidolon,
  Handler's Hound, and Blackwall Seraph remain external named suggestions with
  no Actor UUID.
- Redundant legacy Class subclass arrays and empty Feature defaults have been
  removed. Daggerheart's own migration handles legacy Armor and Action data.

## Compatibility and installation

The manifest declares Foundry **14.x** and Daggerheart **2.x** compatibility.
For the tested target, install with the manifest URL:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Back up existing worlds before moving from the Foundry 13 / Daggerheart 1.2
release line. Upgrade a **copy** of a legacy world and allow Daggerheart's
historical world migration to finish before continuing play.
