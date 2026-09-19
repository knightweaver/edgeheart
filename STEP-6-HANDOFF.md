# Step 6 Handoff — Asset Staging and Deterministic Path Rewriting

## Status

**IN PROGRESS — PATH REWRITING COMPLETE / BINARY ART STAGING PENDING**

The deterministic asset deployment layer is now authoritative in GitHub.

GitHub Actions workflow run **35442434292** completed successfully and produced
the source-path rewrite commit:

`d658e28d06e95566979b26afc946f52362ffc346`

## Accepted deterministic deployment manifest

Step 6 generated `build/step6/asset-manifest.json` with exactly **571** required
assets:

- **538** source-document primary images
- **11** native Competency icons
- **22** adversary tokens

An independent cross-check against the accepted Edgeheart Visual Canon v0.1.1
full art manifest confirms a one-to-one match across all 571 expected output
filenames and deployment paths.

## Source-document rewriting

The source tree now uses portable module paths under:

`modules/edgeheart/assets/...`

The rewrite covers:

- all 538 source documents with dedicated artwork;
- all 22 adversary prototype token paths;
- 528 same-document attack/action image references where the source entity's
  primary art is intentionally reused.

Representative examples:

- Weapon:
  `modules/edgeheart/assets/icons/weapons/assault-carbine.webp`
- Competency Card:
  `modules/edgeheart/assets/icons/domains/network/personal-firewall.webp`
- Adversary portrait:
  `modules/edgeheart/assets/icons/adversaries/sitil-security-guard.webp`
- Adversary token:
  `modules/edgeheart/assets/tokens/adversaries/sitil-security-guard-token.png`

## Intentionally generic images

Visual Canon v0.1.1 did not create separate artwork for derived subordinate
Feature documents. Those 100 documents continue to use Daggerheart generic
Feature icons.

Embedded Environment/Adversary features also retain generic Feature art.
Adversary attack actions retain the generic attack icon because no separate
attack-art family was generated.

## Binary staging

The repository currently contains **0 / 571** final generated image binaries.
The image files are produced externally by the accepted Edgeheart art-generation
workflow and must be staged from that output directory.

Run from a local clone of this repository:

```bash
python tools/stage-assets.py /path/to/generated-edgeheart-art --repo .
python tools/validate-asset-paths.py --repo . --require-assets
```

The staging tool accepts a flat or nested generated-art directory and copies the
globally unique v0.1.1 output filenames into their deterministic module paths.

Final validation requires all 571 files and checks format, accepted dimensions,
and PNG transparency capability for all 22 adversary tokens.

## Downstream gate

Do not compile release Compendia until final binary asset qualification passes.
