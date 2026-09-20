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
