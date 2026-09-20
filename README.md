# Edgeheart — Foundry VTT Module

Edgeheart is a Daggerheart extension module built from the validated neutral
Edgeheart extraction corpus.

This repository mirrors the successful organizational grammar of Cybermancy
while pinning schema/runtime behavior to Daggerheart 1.2.7.

## Runtime

- Foundry VTT 13.351
- Daggerheart 1.2.7

See `DEPLOYMENT-CONTRACT.md` for the frozen implementation contract.

## Current status

Steps 1–8 are complete:

1. deployment contract and module architecture;
2. module skeleton;
3. deterministic source-pack transformation;
4. symbolic reference resolution;
5. native Daggerheart Competency registration;
6. complete 582-asset deployment, including SVG Domain glyphs;
7. deterministic compilation and re-extraction validation of all 13 Compendia;
8. clean-world runtime qualification in Foundry 13.351 / Daggerheart 1.2.7.

The manually qualified Edgeheart 0.1.0 runtime candidate SHA-256 is:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

Step 9 is release hardening and publication. The release workflow rebuilds from
the accepted consolidated source package, reruns every deterministic gate, and
refuses publication unless the rebuilt runtime ZIP is byte-for-byte identical
to the Step 8 qualified candidate.

## Build authority

- `src/packs/` — editable Foundry source boundary
- `packs/` — generated LevelDB derivative output
- `assets/` — qualified module artwork
- `build/` — validation/report outputs
- `release/` — derivative runtime packages
- `release-control/` — explicit publication requests

Generated packs and runtime ZIPs are not canonical inputs.
