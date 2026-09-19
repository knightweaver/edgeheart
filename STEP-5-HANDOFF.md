# Step 5 Handoff — Native Competency Registration

## Status

**COMPLETE / AUTHORITATIVE IN GITHUB**

Step 5 implements native registration of the eleven Edgeheart Competencies
through Daggerheart 1.2.7's supported world-scoped Homebrew domain setting.

GitHub Actions workflow run **35414542076** completed successfully. The generated
Step 5 validation commit is:

`a8771570dda5ca48101d00b2e9d2172890171cf6`

## Registered Competencies

- Network
- Assault
- Chrome
- Systems
- Influence
- Ghost
- Frontier
- Medtech
- Aegis
- Redline
- Blackwall

Each Competency preserves its accepted Edgeheart source description, playstyle,
and access text and uses the portable module icon path:

`modules/edgeheart/assets/icons/domains/<id>.webp`

## Runtime behavior

On Foundry `ready`:

- a GM reads Daggerheart's existing Homebrew setting;
- unrelated Homebrew domains are preserved;
- missing Edgeheart Competencies are added;
- exact existing Edgeheart definitions are left unchanged;
- same-ID differing Homebrew domains are treated as conflicts and are not
  overwritten;
- collisions with Daggerheart core domains are rejected;
- registration is validated through `CONFIG.DH.DOMAIN.allDomains()`.

Non-GM clients do not attempt to write world settings. They audit availability
and log a warning if a GM has not yet completed registration.

The module also exposes the registration/audit helpers through
`game.modules.get("edgeheart").api`.

## Accepted validation

- **11** native Competencies defined
- **231** Domain Cards validated
- **21 cards per Competency**
- **9** class Competency mappings validated
- idempotent registration: **PASS**
- unrelated Homebrew preservation: **PASS**
- same-ID conflict preservation: **PASS**
- core-domain collision guard: **PASS**

## Deliberately pending

Step 5 does not yet perform final Foundry runtime qualification. That remains a
release/runtime test after the complete module is built.

The next deployment step is final Edgeheart asset staging and deterministic
asset-path rewriting before Compendium compilation.
