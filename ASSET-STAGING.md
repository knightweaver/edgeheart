# Edgeheart Asset Staging Contract

## Visual authority

Edgeheart artwork uses accepted **Visual Canon v0.1.1** plus the derived
Daggerheart UI-glyph layer defined by Deployment Contract v1.1.

The complete deployment requires **582 assets**:

- 538 source-document primary WebP images
- 11 full-color Competency illustration WebPs
- 11 monochrome Competency SVG UI glyphs
- 22 adversary token PNGs

Derived Class/Subclass/Origin Feature documents do not receive dedicated art and
intentionally retain Daggerheart generic Feature icons.

## Dual-art Competency contract

Each Competency has both:

```text
assets/icons/domains/<competency>.webp   # full illustration
assets/icons/domains/<competency>.svg    # Daggerheart UI glyph
```

The native Daggerheart Homebrew Domain `src` uses the **SVG**. The WebP remains
the full Edgeheart artwork.

Competency SVGs must be normalized to:

- width: 250
- height: 250
- viewBox: `0 0 250 250`
- vector paths only; no embedded raster image
- no script or external resource reference
- `currentColor` used for fill or stroke

## Final module paths

```text
assets/icons/weapons/<slug>.webp
assets/icons/armors/<slug>.webp
assets/icons/loot/<slug>.webp
assets/icons/consumables/<slug>.webp
assets/icons/cyberware/<slug>.webp
assets/icons/classes/<slug>.webp
assets/icons/subclasses/<slug>.webp
assets/icons/life-paths/<slug>.webp
assets/icons/affiliations/<slug>.webp
assets/icons/environments/<slug>.webp
assets/icons/adversaries/<slug>.webp
assets/icons/domains/<competency>.webp
assets/icons/domains/<competency>.svg
assets/icons/domains/<competency>/<card-slug>.webp
assets/tokens/adversaries/<slug>-token.png
```

Foundry references use portable module paths beginning with
`modules/edgeheart/`. World-specific paths are prohibited.

## Staging artwork

After generating `build/step6/asset-manifest.json`:

```bash
python tools/stage-assets.py /path/to/generated-edgeheart-art --repo .
```

For an intentionally incomplete pass:

```bash
python tools/stage-assets.py /path/to/generated-edgeheart-art --repo . --allow-missing
```

To reorganize a flat art folder into the module hierarchy without touching the
repository:

```bash
python tools/organize-artwork.py /path/to/flat-art /path/to/organized-art \
  --manifest build/step6/asset-manifest.json
```

## Final asset qualification

```bash
npm run validate:assets
```

The validator requires all 582 files and checks:

- portable path agreement;
- expected WebP/PNG dimensions;
- transparent PNG capability for all 22 adversary tokens;
- all 11 Competency SVGs are valid 250x250 vector glyphs;
- no raster embedding, scripts, or external resources in SVG glyphs;
- SVG glyphs use `currentColor`;
- source-document image coverage;
- preservation of intentionally generic Feature and adversary attack art.

Do not compile release Compendia until this validation passes.
