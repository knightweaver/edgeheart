# Edgeheart Asset Staging Contract

## Visual authority

Edgeheart artwork uses accepted **Visual Canon v0.1.1**.

The complete deployment requires **571 image assets**:

- 538 source-document primary images
- 11 Competency icons
- 22 adversary tokens

Derived Class/Subclass/Origin Feature documents do not receive dedicated art in
this release and intentionally retain Daggerheart generic Feature icons.

## Final module paths

Primary assets are staged under:

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
assets/icons/domains/<competency>/<card-slug>.webp
assets/tokens/adversaries/<slug>-token.png
```

Foundry JSON always references those files as portable module paths beginning
with:

`modules/edgeheart/`

World-specific paths are prohibited.

## Same-document image reuse

For Weapons, Armors, Loot, Consumables, Cyberware, and Competency Cards, the
same primary image is also used by that document's attack/action entries.

Adversary attack icons remain generic because no separate attack-art assets were
generated. Embedded Adversary and Environment features also retain generic
Daggerheart Feature icons.

## Staging generated artwork

After Step 6 has generated `build/step6/asset-manifest.json`, run:

```bash
python tools/stage-assets.py /path/to/generated-edgeheart-art --repo .
```

The source directory may be flat or nested. The stager matches the globally
unique v0.1.1 output filenames and copies each file into its deterministic module
destination.

For an intentionally incomplete local pass:

```bash
python tools/stage-assets.py /path/to/generated-edgeheart-art --repo . --allow-missing
```

## Final asset qualification

After all generated images are staged:

```bash
npm run validate:assets
```

The validator requires all 571 files and checks:

- required file presence;
- portable module-path agreement;
- expected image format;
- accepted v0.1.1 dimensions;
- transparent PNG capability for all 22 adversary tokens;
- source-document image-path coverage;
- preservation of intentionally generic Feature and adversary attack art.

Do not compile release Compendia until this validation passes.
