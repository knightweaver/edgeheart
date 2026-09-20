# Edgeheart Foundry Build — Step 9 Release Hardening Report

**Status:** PASS

## Published release

Edgeheart **v0.1.0** is published as a normal, non-draft, non-prerelease GitHub
release:

https://github.com/knightweaver/edgeheart/releases/tag/v0.1.0

Release workflow: **35510638082**

## Published assets

- `edgeheart-v0.1.0.zip`
- `module.json`
- `SHA256SUMS.txt`

The published runtime ZIP is the **exact Step 8 manually qualified candidate**.

SHA-256:

`8e9c2fdba53f108d11f48867a4759fcc51b45aba3c2176b40998bb3e11f161c1`

The release `module.json` SHA-256 is:

`f4741768b2ff0d8bf3fd19cb2a01e236d7114b0a1cabc7c118bb2e2b8da454bf`

## Release hardening

The release workflow rebuilds the complete module from the accepted consolidated
source package and reruns the source, reference, Competency, asset, Compendium,
and runtime-package build gates before publication.

During hardening, byte-for-byte rebuild comparison exposed one important
property of Foundry LevelDB output: the thirteen Compendia each generate
ephemeral `LOG` and `LOG.old` files whose bytes vary between compilations.

The release pipeline now treats those files explicitly as non-semantic compiler
logs rather than pretending raw LevelDB output is globally byte-deterministic.

Fresh rebuild comparison against the qualified Step 8 runtime showed:

- ZIP members compared: **676**
- byte-identical members: **650**
- permitted LevelDB log differences: **26**
- forbidden differences: **0**

Every runtime file other than those 26 LevelDB log files was byte-identical.
Compiled Compendia had already passed the 810/810 re-extraction identity test.

The publication policy therefore:

1. requires a fresh successful rebuild;
2. requires all non-log runtime members to match the Step 8 qualified package;
3. publishes the **exact manually qualified Step 8 archive**, not the fresh
   rebuild with different ephemeral log bytes.

## Foundry distribution endpoints

Manifest:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Download:

`https://github.com/knightweaver/edgeheart/releases/download/v0.1.0/edgeheart-v0.1.0.zip`

These are the URLs already declared in the module manifest.

## Acceptance

Step 9 is **PASS**.

The next work unit is Step 10 — Maintenance and Regression Workflow.
