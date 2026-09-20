# Step 9 Handoff — v0.1.0 Release Publication

## Status

**COMPLETE / PUBLISHED**

Edgeheart v0.1.0 is published at:

https://github.com/knightweaver/edgeheart/releases/tag/v0.1.0

The release contains the exact clean-world-qualified Step 8 runtime archive,
plus the Foundry installation manifest and checksums.

Qualified/published runtime SHA-256:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

## Release pipeline rule

Future releases must distinguish canonical/semantic reproducibility from raw
LevelDB log bytes. `LOG` and `LOG.old` are ephemeral LevelDB output and can
vary across compilations. All other runtime members must remain identical when
the source inputs are unchanged, and all compiled packs must continue to pass
re-extraction validation.

## Next

Step 10 should formalize:

- maintenance workflow;
- regression fixtures;
- change-impact rules;
- versioning/release cadence;
- required runtime smoke tests for content and tooling changes.
