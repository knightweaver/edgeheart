# Edgeheart 0.2.0 migration coverage audit

Target: Foundry 14.368, Daggerheart 2.10.5 (`Foundryborne/daggerheart` tag `2.10.5`, commit `6bf4b69f983139107bd0d2207a5b2897e8c44cc1`). Its `system.json` declares minimum 14.364, verified 14.368, maximum 14. Legacy release `v0.1.1` remains frozen.

The Edgeheart manifest declares major-version compatibility (Foundry 14,
Daggerheart 2), following the established module convention. The exact target
builds above remain pending runtime qualification; the broad manifest range
does not establish qualification on every earlier patch in those generations.

Classification: **A** = Daggerheart explicitly migrates the old shape; **B** = Edgeheart must normalize its projection; **C** = preserve pending runtime evidence. This audit concerns new module Compendia and separately notes that Daggerheart's world migration depends on the world's recorded system version.

| Difference | Classification | Evidence and decision |
| --- | --- | --- |
| Armor `baseScore` and `marks` → `armor.max/current` | A | `module/data/item/armor.mjs` `migrateDocumentData` maps both. Preserve legacy data pending runtime test; do not hand-convert. |
| Action `damage.parts` → `damage.main/resources` | A | `module/data/action/baseAction.mjs` `migrateData` maps array parts, then the keyed parts into main/resources. Preserve source until runtime test. |
| Environment `system.features[]` → embedded `items[]` | B | `module/data/actor/environment.mjs` reads `parent.items` for features; no Environment conversion in `module/systemRegistration/migrations.mjs` or its handlers. 15 actors have 49 legacy features and no embedded features. |
| Environment impulses array → string | B | `environment.mjs` defines `impulses: StringField`. Join the ordered strings without dropping text. |
| Environment potential adversary name array → keyed `{label, adversaries: [UUID]}` | B | `environment.mjs` requires the keyed field. Exact matches to the 22 Edgeheart Actors become Compendium UUIDs. By explicit user decision, three unmatched names in five occurrences remain labeled external suggestions with empty UUID arrays. |
| Legacy Environment feature auxiliary fields | B | All 49 have empty `cost`, `effects`, `range`; `uses` is the same empty/default object; `target` is `scene` with null amount. Preserve IDs, names, descriptions, images and passive/action/reaction forms in native Feature Items. No non-default auxiliary data exists. |
| Class `system.subclasses` | B | `module/data/item/class.mjs` omits the field and `fetchSubclasses()` discovers them through Subclass `linkedClass`. All 18 current Subclasses have linkedClass. Remove the redundant generated arrays and 18 corresponding symbolic references. |
| Standalone Feature `originItemType`, `multiclassOrigin`, `identifier` | B for empty defaults; C for nonempty | 100 Feature documents examined: no populated legacy value. `module/data/item/feature.mjs` defines `granter` and `featureForm`; remove only empty defaults. Do not guess granter for future populated values. |
| Domain configuration | C | `module/config/domainConfig.mjs` includes `dread` and `allDomains()` combines homebrew and core. Edgeheart registration needs runtime verification; no speculative rewrite. Validator must include Dread. |
| `_stats` target runtime | B | Build output currently writes Foundry 13.351 and DH 1.2.7. Set generated source metadata to 14.368 / 2.10.5. This does not qualify runtime behavior. |
| Other Actor/Item shape and Foundry runtime behavior | C | Preserve source until clean-world test identifies a mismatch. |

## External named suggestions

| Environment | Name absent from Edgeheart Adversary pack |
| --- | --- |
| Highway Kill Run | Cordon Eidolon |
| Blackwall Storm Highway | Handler's Hound; Blackwall Seraph |
| Blacksite Extraction | Cordon Eidolon |
| Dead Pantheon Breach | Blackwall Seraph |

The five occurrences retain their labels in native keyed groups with `adversaries: []`; no Actor UUID is invented. The projection rejects any additional unmatched name, so future additions require an explicit decision.

## Runtime gate

The v0.2.0 clean-world checklist was reported PASS on 2026-09-24. The baseline remains a pending candidate until the copied-world upgrade test passes. Do not mark overall qualification PASS, publish a release, or merge it before then. Daggerheart's system migration chain is tested on the copied world, not simulated by rewriting its records in this repository.
