# Edgeheart source package

Place the accepted consolidated extraction package here as:

`sources/edgeheart-consolidated-production-v1.0.zip`

This ZIP is the canonical Step 3 transformation input named in
`DEPLOYMENT-CONTRACT.md`.

Pushing that exact path to `main` triggers the source-pack generation workflow,
which regenerates `src/packs/`, writes the Step 3 build reports, validates the
result, and commits the generated source-pack JSON back to `main`.
