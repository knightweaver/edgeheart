# Edgeheart v0.1.1 — Final Foundry 13 / Daggerheart 1.2 Release

This is the final legacy-series Edgeheart release before migration work begins
for Foundry 14 / Daggerheart 2.x.

## Compatibility metadata

The runtime content is unchanged from v0.1.0. This release broadens the package
manifest so routine point/build updates do not unnecessarily make the module
uninstallable:

- Foundry VTT: **13.x**
- Daggerheart: **1.2.x**

The implementation was originally validated on Foundry 13.351 and Daggerheart
1.2.7.

The Daggerheart relationship intentionally has no hard maximum. A literal
`maximum: 1.2` can compare as older than a patch release such as 1.2.7 and
could incorrectly block the exact tested system version.

## Installation

Current/latest legacy release:

`https://github.com/knightweaver/edgeheart/releases/latest/download/module.json`

Tagged releases remain directly addressable by replacing `latest` with the
desired release tag.

## Content

No Edgeheart rules, Compendium entities, IDs, artwork, runtime scripts, or
mechanics were changed in this release.
