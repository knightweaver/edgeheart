# Step 6 Handoff — Asset Staging and Deterministic Path Rewriting

## Status

**COMPLETE / AUTHORITATIVE IN GITHUB**

Step 6 is complete under Deployment Contract v1.1.

GitHub Actions workflow run **35485972593** generated the approved Competency
SVG glyphs, refreshed the deterministic asset manifest, required all staged
assets, validated raster/SVG structure, and committed the final asset set.

The final generated asset commit is:

`d7935adc0807e65dc1f1237703d883ff57ec328b`

## Final asset inventory

The complete Step 6 deployment contains **582 required assets**:

- **538** source-document primary images
- **11** Competency full-color WebP illustrations
- **11** Competency 250x250 SVG UI glyphs
- **22** adversary token PNGs

Final qualification result:

- Assets present: **582 / 582**
- Assets missing: **0**
- Competency SVG structure: **PASS**
- Adversary token transparency capability: **PASS**
- Expected raster dimensions: **PASS**
- Portable module-path agreement: **PASS**
- Source-document image coverage: **PASS**

## Dual-art Competency contract

Each Competency now has both:

```text
assets/icons/domains/<domain>.webp   # full Edgeheart illustration
assets/icons/domains/<domain>.svg    # Daggerheart interface glyph
```

Daggerheart 1.2.7 Homebrew Domain `src` uses the SVG UI glyph.

The 231 Competency Cards continue to use nested WebP artwork under:

`assets/icons/domains/<domain>/<card-slug>.webp`

The eleven SVG glyphs were converted from the approved visual concepts into
clean geometric vector assets optimized for small Daggerheart UI rendering.

## Intentional generic artwork

The following remain on Daggerheart generic icons by design:

- 100 derived Class/Subclass/Origin Feature documents
- embedded Environment/Adversary features
- adversary attack icons

No dedicated Visual Canon v0.1.1 artwork exists for those sub-elements.

## Downstream gate

The asset gate is cleared.

The next build unit is deterministic LevelDB Compendium compilation from the
accepted `src/packs/` source tree, followed by compiled-pack validation and
clean-world Foundry 13.351 / Daggerheart 1.2.7 runtime qualification.
