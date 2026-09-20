# Edgeheart Step 8 — Clean-World Runtime Qualification

## Purpose

This is the first qualification performed inside the actual target runtime. The
build pipeline has already validated source structure, references, native
Competency registration logic, all 582 assets, and all thirteen compiled
LevelDB packs.

Runtime target:

- Foundry VTT **13.351**
- Daggerheart **1.2.7**
- Edgeheart **0.1.0**

Use a clean test world so existing Homebrew domains, modules, and world content
cannot mask Edgeheart defects.

## Installation

1. Create or use a Foundry 13.351 data directory with Daggerheart 1.2.7.
2. Extract `edgeheart-v0.1.0.zip` into:
   `Data/modules/edgeheart/`
3. Confirm the resulting path is:
   `Data/modules/edgeheart/module.json`
4. Launch Foundry, create a new Daggerheart world, and enable only Edgeheart as
   the non-system module.
5. Enter the world as a GM.

## Gate A — startup and Competencies

Pass conditions:

- no Edgeheart JavaScript error during `init` or `ready`;
- Edgeheart reports successful/already-registered Competency status;
- the eleven Competencies exist in Daggerheart Homebrew domains;
- Network, Assault, Chrome, Systems, Influence, Ghost, Frontier, Medtech,
  Aegis, Redline, and Blackwall all display their SVG glyphs;
- glyphs render cleanly in the character-sheet Domain area in both available
  Daggerheart themes;
- no full-color Competency WebP is being used as the 20×20 interface glyph.

## Gate B — Compendia

All thirteen packs must open without error:

- Weapons — 64 documents
- Armors — 25
- Loot — 40
- Consumables — 40
- Cyberware — 60
- Classes — 9
- Subclasses — 18
- Competencies — 231 Domain Cards
- Features — 100
- Life Paths — 6
- Affiliations — 8
- Adversaries — 22
- Environments — 15

Internal Compendium folders are additional structural records and are not
included in the document counts above.

## Gate C — representative document rendering

Open at least one document from every pack and confirm:

- sheet renders without console/schema errors;
- primary art renders;
- attack/action controls render where applicable;
- descriptions and source text remain intact.

Specifically include:

- Runner class;
- Breach Specialist and Net Diver subclasses;
- one Network Domain Card;
- Military Surplus Life Path;
- Corporate Asset Affiliation;
- Sitil Security Guard adversary;
- Neon Night Market environment.

For Sitil Security Guard, verify the embedded Feature Items render and can be
expanded/used normally. This directly exercises the embedded Actor export-key
correction discovered during Step 7.

## Gate D — reference behavior

On a test character:

1. Add an Edgeheart Class and verify its linked subclass options resolve.
2. Add a linked Subclass and verify its Feature links resolve.
3. Add a Life Path and Affiliation and verify their Features resolve.
4. Add Domain Cards from the class Competency and verify Daggerheart recognizes
   the custom Domain ID.
5. Confirm Domain glyphs are visible in the character header.

## Gate E — Actor behavior

Instantiate representative Adversary and Environment documents into the world.

Pass conditions:

- Actor creation succeeds;
- adversary portrait and transparent token render;
- adversary embedded Features survive instantiation;
- adversary attack data renders;
- Environment sheet opens with all inline environment features;
- no missing-UUID or malformed-action errors appear in the console.

## Gate F — clean-console sweep

After the tests above:

- reload the world;
- reopen representative sheets;
- review browser console for Edgeheart/Daggerheart exceptions;
- verify there are no 404 requests for `modules/edgeheart/assets/...`;
- verify there are no unresolved Compendium UUID warnings.

Record any failure with the exact console message, document name, and action that
triggered it before modifying source data.

## Acceptance

Step 8 passes only when all gates above succeed in the exact frozen runtime.
Passing source/compile validation alone does not substitute for this runtime
qualification.
