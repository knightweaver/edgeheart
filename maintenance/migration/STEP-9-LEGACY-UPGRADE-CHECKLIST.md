# Edgeheart 0.2.0 copied-world upgrade gate

Clean-world qualification was reported PASS on 2026-09-24 for the candidate from
[Actions run 36048884506](https://github.com/knightweaver/edgeheart/actions/runs/36048884506):
`edgeheart-runtime-candidate-v0.2.0`, inner `edgeheart-v0.2.0.zip` SHA-256
`0170e923c2ea773f334933d993a8ee3bca685e3ed067af57002d642ea34c3e1c`.
The user authorized a clean-world-only release on 2026-09-24. This upgrade
test remains useful before moving an existing campaign, but was not completed
as part of the v0.2.0 release qualification.

1. Back up the known-good Foundry **13.351 / Daggerheart 1.2.7** Data directory.
   Make a separate copy of its world, retaining its settings and documents.
   Leave the original world untouched.
2. On an isolated Foundry **14.368** installation, install Daggerheart
   **2.10.5** and the **same Edgeheart candidate** above. Extract the inner ZIP
   into `Data/modules/edgeheart/` with `module.json` at that directory's root.
   Check the ZIP's SHA-256 before use. Open only the copied world, and allow
   Daggerheart's normal historical migrations to finish before inspecting data.
3. Record Foundry, Daggerheart, and Edgeheart versions, migration completion,
   and browser/server console output. Confirm the copied world's existing
   characters, Items, Actors, scenes, and settings remain accessible. In
   particular, inspect a pre-existing Armor's slots and an Action with damage.
4. Repeat the [clean-world checklist](../RUNTIME-SMOKE-TESTS.md):
   open all 13 Compendia; exercise Character Builder and the 11 Domains;
   inspect a representative adversary attack; inspect the Environment's
   embedded Features, impulses, and potential adversaries. The three unmatched
   names (Cordon Eidolon, Handler's Hound, Blackwall Seraph) remain external
   named suggestions with no Actor UUID.
5. Compare behavior against the passing clean world. Reload once. Report any
   migration errors, broken UUIDs, missing images, lost values, or console
   errors; include logs or screenshots for failures.

Report **PASS** only if the copy migrates and these checks pass. Include the
candidate SHA-256 and actual runtime versions with the result. Record any
subsequent PASS separately from the clean-world-only release qualification.
