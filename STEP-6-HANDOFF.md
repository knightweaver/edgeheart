# Step 6 Handoff — Asset Staging and Deterministic Path Rewriting

## Status

**IN PROGRESS — 571 RASTER ASSETS STAGED / 11 SVG UI GLYPHS PENDING**

Deployment Contract v1.1 formalizes the dual-art Competency/Domain requirement.

## Asset inventory

The complete Step 6 deployment now contains **582 required assets**:

- **538** source-document primary images
- **11** Competency full-color WebP illustrations
- **11** Competency 250x250 SVG UI glyphs
- **22** adversary tokens

The previously generated 571 raster assets (549 WebPs + 22 PNG tokens) have been
staged in GitHub. The remaining deployment work is generation and staging of the
11 derived SVG UI glyphs.

## Domain runtime behavior

Daggerheart 1.2.7 Homebrew Domain `src` now points to:

`modules/edgeheart/assets/icons/domains/<domain>.svg`

The corresponding full-color illustration remains:

`modules/edgeheart/assets/icons/domains/<domain>.webp`

Existing Edgeheart world settings that contain the old WebP `src` are migrated
to the SVG path only when the rest of the Competency definition is an exact
Edgeheart match. Differing same-ID Homebrew domains remain protected as
conflicts and are never silently overwritten.

## Source-document rewriting

The 538 Foundry documents continue to use their full-color primary artwork.
The 231 Competency Cards continue to use nested WebP art under:

`assets/icons/domains/<domain>/<card-slug>.webp`

No Domain Card JSON changes are required for the SVG UI-glyph layer.

## SVG qualification

Each of the eleven SVG glyphs must have:

- `width="250"`
- `height="250"`
- `viewBox="0 0 250 250"`
- at least one vector `<path>`
- no embedded raster `<image>`
- no script or external resource reference
- `currentColor` fill or stroke

Final validation:

```bash
npm run validate:assets
```

## Downstream gate

Do not compile release Compendia until all 582 assets pass final qualification.
