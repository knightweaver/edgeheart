/**
 * Edgeheart Competency registration for Daggerheart 1.2.7.
 *
 * Daggerheart 1.2.7 exposes custom Domains through the world-scoped Homebrew
 * setting. CONFIG.DH.DOMAIN.allDomains() merges those Homebrew domains with
 * the nine core Daggerheart domains. Edgeheart therefore registers its
 * Competencies through that supported setting rather than patching Daggerheart.
 *
 * Descriptions below preserve the three source-backed Competency paragraphs
 * from the accepted Edgeheart neutral corpus: description, playstyle, access.
 */

export const EDGEHEART_COMPETENCIES = Object.freeze({
  network: Object.freeze({
    id: "network",
    label: "Network",
    src: "modules/edgeheart/assets/icons/domains/network.webp",
    description:
      "<p>Network is the Competency of hacking, electronic warfare, artificial intelligence, signal manipulation, and remote systems.</p>" +
      "<p>Characters who use Network bend the world through code, hijacked infrastructure, predictive software, signal ghosts, drones, cyberdecks, and forbidden protocols.</p>" +
      "<p>Network is commonly accessed through cyberdecks, neural interfaces, signal rigs, AI assistants, Eidolon uplinks, and military-grade intrusion suites.</p>"
  }),
  assault: Object.freeze({
    id: "assault",
    label: "Assault",
    src: "modules/edgeheart/assets/icons/domains/assault.webp",
    description:
      "<p>Assault is the Competency of direct combat, firearms, blades, heavy weapons, combat reflexes, battlefield aggression, and tactical violence.</p>" +
      "<p>Characters who use Assault solve problems through superior firepower, brutal precision, weapon mastery, and the willingness to keep moving when anyone else would be dead.</p>" +
      "<p>Assault is commonly accessed through combat training, smartgun links, weapon implants, reflex boosters, cyberlimb weapon mounts, and Eidolon weapon systems.</p>"
  }),
  chrome: Object.freeze({
    id: "chrome",
    label: "Chrome",
    src: "modules/edgeheart/assets/icons/domains/chrome.webp",
    description:
      "<p>Chrome is the Competency of reinforced bodies, synthetic muscle, subdermal armor, cybernetic reflexes, implanted combat systems, and physical control.</p>" +
      "<p>Characters who use Chrome turn their body into a weapon platform and survive through precision, endurance, and engineered durability.</p>" +
      "<p>Chrome is commonly accessed through combat augments, reinforced bones, armored skin, reflex boosters, synthetic organs, and military-grade body modification.</p>"
  }),
  systems: Object.freeze({
    id: "systems",
    label: "Systems",
    src: "modules/edgeheart/assets/icons/domains/systems.webp",
    description:
      "<p>Systems is the Competency of engineering, drones, scanners, gadgets, tactical preparation, hardware, and battlefield tools.</p>" +
      "<p>Characters who use Systems solve problems by having the right device, the right schematic, or the right plan at the right time.</p>" +
      "<p>Systems is commonly accessed through drone rigs, engineering kits, tactical scanners, field printers, maintenance tools, and Eidolon support systems.</p>"
  }),
  influence: Object.freeze({
    id: "influence",
    label: "Influence",
    src: "modules/edgeheart/assets/icons/domains/influence.webp",
    description:
      "<p>Influence is the Competency of reputation, negotiation, manipulation, media presence, corporate pressure, social engineering, and contacts.</p>" +
      "<p>Characters who use Influence understand that power is not always held by the person with the biggest gun, but by who controls the story.</p>" +
      "<p>Influence is commonly accessed through reputation, media implants, voice modulators, corporate credentials, fake identities, social networks, and blackmail archives.</p>"
  }),
  ghost: Object.freeze({
    id: "ghost",
    label: "Ghost",
    src: "modules/edgeheart/assets/icons/domains/ghost.webp",
    description:
      "<p>Ghost is the Competency of infiltration, stealth, assassination, sabotage, disguise, theft, and black operations.</p>" +
      "<p>Characters who use Ghost disappear into blind spots, false identities, smoke, shadow, dead cameras, and the moment between one heartbeat and the next.</p>" +
      "<p>Ghost is commonly accessed through optical camouflage, ghost skin, stealth implants, lockpicks, false-face rigs, suppressed weapons, and black ops suites.</p>"
  }),
  frontier: Object.freeze({
    id: "frontier",
    label: "Frontier",
    src: "modules/edgeheart/assets/icons/domains/frontier.webp",
    description:
      "<p>Frontier is the Competency of survival, navigation, tracking, wasteland, environments, and life beyond corporate control.</p>" +
      "<p>Characters who use Frontier know how to cross dead zones, read broken streets, survive toxic storms, track enemies through ruins, and find paths where maps have failed.</p>" +
      "<p>Frontier is commonly accessed through nomad training, survival gear, environmental suits, tracking drones, and off-grid vehicles.</p>"
  }),
  medtech: Object.freeze({
    id: "medtech",
    label: "Medtech",
    src: "modules/edgeheart/assets/icons/domains/medtech.webp",
    description:
      "<p>Medtech is the Competency of trauma care, surgery, emergency medicine, nanomedicine, cyberware repair, biological support, and keeping people alive after they should be dead.</p>" +
      "<p>Characters who use Medtech carry biofoam, trauma patches, surgical drones, stimulant cocktails, organ printers, and the kind of calm hands people pray for when bullets start flying.</p>" +
      "<p>Medtech is commonly accessed through trauma kits, combat medic rigs, and emergency life-support implants.</p>"
  }),
  aegis: Object.freeze({
    id: "aegis",
    label: "Aegis",
    src: "modules/edgeheart/assets/icons/domains/aegis.webp",
    description:
      "<p>Aegis is the Competency of protection, defense, armor, shields, suppression, tactical cover, and keeping the team alive under fire.</p>" +
      "<p>Characters who use Aegis turn themselves into the line between their allies and the thing trying to kill them.</p>" +
      "<p>Aegis is commonly accessed through heavy armor, riot shields, defensive drones, barrier systems, squad command uplinks, and Eidolon shielding.</p>"
  }),
  redline: Object.freeze({
    id: "redline",
    label: "Redline",
    src: "modules/edgeheart/assets/icons/domains/redline.webp",
    description:
      "<p>Redline is the Competency of overclocked bodies, experimental drugs, aggressive nanites, unstable augments, combat highs, mutation, pain loops, and controlled cyberpsychosis.</p>" +
      "<p>Characters who use Redline turn their body and mind into fuel, pushing beyond safe limits and daring the crash to catch them later.</p>" +
      "<p>Redline is commonly accessed through combat injectors, illegal biomods, berserker suites, psychoactive augments, neural accelerants, and corporate black-lab procedures.</p>"
  }),
  blackwall: Object.freeze({
    id: "blackwall",
    label: "Blackwall",
    src: "modules/edgeheart/assets/icons/domains/blackwall.webp",
    description:
      "<p>Blackwall is the Competency of forbidden AI, rogue daemons, impossible code, digital possession, haunted machines, Eidolon minds, and things sealed beyond the network.</p>" +
      "<p>Characters who use Blackwall do not simply access technology. They listen to something on the other side, and sometimes it answers.</p>" +
      "<p>Blackwall is commonly accessed through illegal cyberdecks, corrupted neural links, Eidolon interfaces, AI fragments, forbidden daemons, Collapse relics, and contact with the Black Wall itself.</p>"
  })
});

const comparableDomain = domain => ({
  id: domain?.id ?? "",
  label: domain?.label ?? "",
  src: domain?.src ?? "",
  description: domain?.description ?? ""
});

const domainEquals = (a, b) =>
  JSON.stringify(comparableDomain(a)) === JSON.stringify(comparableDomain(b));

/**
 * Pure planning function used by both runtime registration and build validation.
 * Existing unrelated Homebrew domains are preserved. Edgeheart never silently
 * overwrites a same-id Homebrew domain whose data differs from its definition.
 */
export function planCompetencyRegistration({
  coreDomains = {},
  homebrewDomains = {}
} = {}) {
  const nextDomains = Object.fromEntries(
    Object.entries(homebrewDomains).map(([id, value]) => [id, { ...value }])
  );
  const added = [];
  const unchanged = [];
  const conflicts = [];
  const coreConflicts = [];

  for (const [id, expected] of Object.entries(EDGEHEART_COMPETENCIES)) {
    if (Object.prototype.hasOwnProperty.call(coreDomains, id)) {
      coreConflicts.push(id);
      continue;
    }

    const existing = homebrewDomains[id];
    if (!existing) {
      nextDomains[id] = { ...expected };
      added.push(id);
      continue;
    }

    if (domainEquals(existing, expected)) {
      unchanged.push(id);
      continue;
    }

    conflicts.push({
      id,
      expected: comparableDomain(expected),
      existing: comparableDomain(existing)
    });
  }

  return {
    nextDomains,
    added,
    unchanged,
    conflicts,
    coreConflicts,
    changed: added.length > 0
  };
}

export function auditEdgeheartCompetencies(allDomains = {}) {
  const missing = [];
  const mismatched = [];

  for (const [id, expected] of Object.entries(EDGEHEART_COMPETENCIES)) {
    const actual = allDomains[id];
    if (!actual) {
      missing.push(id);
      continue;
    }
    if (!domainEquals(actual, expected)) {
      mismatched.push(id);
    }
  }

  return {
    valid: missing.length === 0 && mismatched.length === 0,
    missing,
    mismatched
  };
}

/**
 * Persist Edgeheart Competencies into Daggerheart's native world-scoped
 * Homebrew setting. This requires a GM. Non-GM clients only audit availability.
 */
export async function registerEdgeheartCompetencies({ notify = true } = {}) {
  if (!globalThis.game || !globalThis.CONFIG?.DH) {
    throw new Error("Edgeheart Competencies require an initialized Daggerheart world.");
  }

  const settingNamespace = CONFIG.DH.id;
  const settingKey = CONFIG.DH.SETTINGS.gameSettings.Homebrew;
  const currentModel = game.settings.get(settingNamespace, settingKey);
  const current = currentModel?.toObject
    ? currentModel.toObject()
    : structuredClone(currentModel ?? {});
  const homebrewDomains = current.domains ?? {};
  const coreDomains = CONFIG.DH.DOMAIN.domains ?? {};

  const plan = planCompetencyRegistration({ coreDomains, homebrewDomains });

  if (plan.coreConflicts.length) {
    const message =
      `Edgeheart | Cannot register Competencies because IDs collide with Daggerheart core domains: ${plan.coreConflicts.join(", ")}`;
    console.error(message);
    if (notify && game.user?.isGM) ui.notifications?.error(message);
    return { status: "core-conflict", ...plan };
  }

  if (plan.conflicts.length) {
    const ids = plan.conflicts.map(entry => entry.id);
    const message =
      `Edgeheart | Existing Homebrew domains conflict with Edgeheart Competencies: ${ids.join(", ")}. Existing world data was preserved.`;
    console.warn(message, plan.conflicts);
    if (notify && game.user?.isGM) ui.notifications?.warn(message);
    return { status: "homebrew-conflict", ...plan };
  }

  if (!game.user?.isGM) {
    const audit = auditEdgeheartCompetencies(CONFIG.DH.DOMAIN.allDomains());
    if (!audit.valid) {
      console.warn(
        "Edgeheart | Competencies are not fully registered. A GM must enter the world with Edgeheart enabled.",
        audit
      );
    }
    return {
      status: audit.valid ? "already-registered" : "gm-required",
      ...plan,
      audit
    };
  }

  if (plan.changed) {
    await game.settings.set(settingNamespace, settingKey, {
      ...current,
      domains: plan.nextDomains
    });
  }

  const audit = auditEdgeheartCompetencies(CONFIG.DH.DOMAIN.allDomains());
  if (!audit.valid) {
    const message =
      `Edgeheart | Competency registration did not validate. Missing: ${audit.missing.join(", ") || "none"}; mismatched: ${audit.mismatched.join(", ") || "none"}.`;
    console.error(message, audit);
    if (notify) ui.notifications?.error(message);
    return { status: "validation-failed", ...plan, audit };
  }

  console.info(
    `Edgeheart | Competencies ready (${Object.keys(EDGEHEART_COMPETENCIES).length}); added ${plan.added.length}, unchanged ${plan.unchanged.length}.`
  );

  return {
    status: plan.changed ? "registered" : "already-registered",
    ...plan,
    audit
  };
}
