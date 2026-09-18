# Step 3 Handoff — Deterministic Source-Pack Transformation

## Status

Step 3 is implemented and locally validated against the accepted
`edgeheart-consolidated-production-v1.0.zip` input.

The GitHub repository now contains the deterministic builder, validator, and an
Actions workflow that will populate the authoritative `src/packs/` tree when
the canonical ZIP is added at:

`sources/edgeheart-consolidated-production-v1.0.zip`

## Accepted output

- **638** Foundry documents
- **172** structural Compendium folders
- **810** generated pack-source JSON files total
- **145** intentionally unresolved references inventoried for Step 4
- **0** unknown internal reference targets
- **0** stable-ID collisions
- **0** `system.actions` shape errors

The accepted source archive SHA-256 is:

`3943cf9957661c82add6ecbaac33a3ecb8a80f1dc1b2d3161b1ba6f3590d32fa`

The workflow verifies this checksum before generating or committing source-pack
JSON.

## Step 3 boundaries

Step 3 assigns deterministic Foundry IDs, establishes the Compendium folder
structure, and preserves source/bundle provenance. It deliberately does not:

- resolve symbolic Class/Subclass/Origin references;
- populate Class `system.subclasses` from bundle membership;
- convert pending class Competency mappings into final `system.domains` values;
- register Daggerheart Homebrew domains;
- replace placeholder art paths with final Edgeheart assets;
- compile LevelDB Compendia.

Step 4 resolves the symbolic bundle relationships and class Competency mappings
before Compendium compilation.
