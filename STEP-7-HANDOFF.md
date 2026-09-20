# Step 7 Handoff — Compendium Compilation and Runtime Candidate

## Status

**COMPLETE / AUTHORITATIVE IN GITHUB**

Step 7 deterministically compiles all thirteen declared Edgeheart Compendia with
`@foundryvtt/foundryvtt-cli`, re-extracts every compiled pack, and verifies
stable source identity before producing a clean-world runtime candidate.

Final successful workflow:

- GitHub Actions run: **35486375897**
- Step 7 report commit: **6a9e7039b1ff430b41880c6c4e76d2edd3b55aa5**

## Compendium qualification

- Declared Compendia: **13**
- Source pack entries: **810**
- Re-extracted compiled entries: **810**
- Stable-ID/name/type/folder identity comparison: **PASS**
- Compiled adversaries: **22**
- Compiled environments: **15**

Generated LevelDB packs remain derivative output and are not committed as
canonical source.

## Actor export-key correction

The first compilation attempt exposed a structural omission in the upstream
Edgeheart Actor payloads: embedded adversary Feature Items had stable `_id`
values but lacked Foundry export `_key` metadata.

Daggerheart 1.2.7 official Actor pack sources use:

```text
!actors.items!<actor-id>.<item-id>
!actors.items.effects!<actor-id>.<item-id>.<effect-id>
```

The Edgeheart source builder and source validator now reproduce and enforce this
official grammar. Current Actor sources were repaired without changing any
mechanics or stable IDs. After that correction all thirteen Compendia compiled
successfully.

## Runtime candidate

The deterministic runtime candidate is:

`edgeheart-v0.1.0.zip`

Qualification metadata:

- Runtime files: **676**
- Runtime art assets: **582**
- Compiled Compendia: **13**
- SHA-256:
  `8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

The runtime archive contains only `module.json`, runtime scripts, the qualified
asset tree, and compiled LevelDB packs. Source packages, editable JSON, developer
tooling, and node dependencies are excluded.

## Next gate

Step 8 is clean-world runtime qualification against exactly:

- Foundry VTT **13.351**
- Daggerheart **1.2.7**
- Edgeheart **0.1.0**

See `RUNTIME-QUALIFICATION.md`.
