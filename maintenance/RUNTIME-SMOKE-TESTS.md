# Edgeheart Runtime Smoke-Test Matrix

| Change | Minimum manual Foundry check |
| --- | --- |
| Documentation/reports only | None |
| Artwork replacement at same path | Targeted smoke of affected document/UI |
| Item content correction | Open affected pack/item; exercise actions if present |
| Class/Subclass/Origin correction | Full Character Builder path for affected option |
| Competency/Card correction | Character Builder + Domain SVG + affected Card |
| Adversary correction | Instantiate Actor; embedded Features, attack, token |
| Environment correction | Open/instantiate Environment and all inline Features |
| Runtime script/Homebrew Domain change | Full clean-world qualification |
| Module/Compendium contract change | Full clean-world qualification |
| Canonical corpus addition/removal | Full clean-world qualification |
| Runtime target change | Full clean-world qualification plus migration review |

Preferred regression representatives are defined in
`maintenance/regression-fixtures-v1.json`. If the changed entity is not one of
those fixtures, exercise the changed entity in addition to the relevant fixture.

## v0.2.0 clean-world gate — Foundry 14.368 / Daggerheart 2.10.5

Download the Actions `edgeheart-runtime-candidate-v0.2.0` artifact. Extract its
inner `edgeheart-v0.2.0.zip` into Foundry's user Data `modules/edgeheart/`
directory so `module.json` sits directly in that directory, then restart
Foundry. Enable Edgeheart in Manage Modules; reinstalling may leave it unchecked.
Report the actual Foundry and Daggerheart versions and the candidate SHA-256.

1. Confirm Edgeheart activates without a module error and all 13 Compendia open.
2. Open a Weapon, an Armor, and a Feature with a damage Action; exercise the
   Action and check Armor slots. Verify artwork and inspect the browser console.
3. Open Runner and both linked Subclasses. Create a character and exercise the
   Class/Subclass, Life Path, Affiliation and Competency/Domain selection path.
   Confirm all 11 custom Domains, their glyphs, and a representative card work.
4. Instantiate Sitil Security Guard and exercise its attack and embedded Feature.
5. Open and instantiate Neon Night Market and Blackwall Storm Highway. Verify
   embedded Features, their text and passive/action/reaction forms. Inspect
   potential adversaries: matching names link to Actors, while Handler's Hound
   and Blackwall Seraph remain named suggestions without Actor links. Inspect
   Highway Kill Run for Cordon Eidolon under the same rule.
6. Reload and report any browser console errors/warnings, broken UUIDs, missing
   images, or lost data; include screenshots and console output for failures.

Mark clean-world qualification PASS only after these runtime results are reported.
Then upgrade a **copy** of a known-good Foundry 13 / Daggerheart 1.2.7 world to
Foundry 14.368 / Daggerheart 2.10.5 with the v0.2.0 candidate. Allow
Daggerheart to perform its historical migrations before examining content.
Repeat the checks above, compare behavior to the clean world, and report any
migration errors. Do not modify the original world.
