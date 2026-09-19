#!/usr/bin/env node

import { promises as fs } from "node:fs";
import path from "node:path";
import {
  EDGEHEART_COMPETENCIES,
  planCompetencyRegistration
} from "../scripts/competencies.js";

const ROOT = process.cwd();
const REPORT_DIR = path.join(ROOT, "build", "step5");

const EXPECTED_IDS = [
  "network",
  "assault",
  "chrome",
  "systems",
  "influence",
  "ghost",
  "frontier",
  "medtech",
  "aegis",
  "redline",
  "blackwall"
];

const CORE_DAGGERHEART_127_DOMAINS = {
  arcana: {},
  blade: {},
  bone: {},
  codex: {},
  grace: {},
  midnight: {},
  sage: {},
  splendor: {},
  valor: {}
};

const EXPECTED_CLASS_DOMAINS = {
  "class:augmented": ["chrome"],
  "class:broker": ["influence"],
  "class:infiltrator": ["ghost"],
  "class:reclaimer": ["frontier"],
  "class:runner": ["network"],
  "class:solo": ["assault"],
  "class:tech": ["systems"],
  "class:trauma-doc": ["medtech"],
  "class:warden": ["aegis"]
};

const errors = [];

function assert(condition, message) {
  if (!condition) errors.push(message);
}

async function loadJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function sourceDocuments(directory) {
  const names = await fs.readdir(directory);
  const docs = [];
  for (const name of names.sort()) {
    if (!name.endsWith(".json")) continue;
    const doc = await loadJson(path.join(directory, name));
    if (String(doc._key ?? "").startsWith("!folders!")) continue;
    docs.push({ name, doc });
  }
  return docs;
}

const ids = Object.keys(EDGEHEART_COMPETENCIES);
assert(ids.length === 11, `expected 11 Competencies, got ${ids.length}`);
assert(
  JSON.stringify(ids) === JSON.stringify(EXPECTED_IDS),
  `Competency IDs/order differ from accepted contract: ${ids.join(", ")}`
);

for (const id of EXPECTED_IDS) {
  const competency = EDGEHEART_COMPETENCIES[id];
  assert(Boolean(competency), `missing Competency definition: ${id}`);
  if (!competency) continue;
  assert(competency.id === id, `${id}: definition.id mismatch`);
  assert(Boolean(competency.label), `${id}: empty label`);
  assert(
    competency.src === `modules/edgeheart/assets/icons/domains/${id}.webp`,
    `${id}: asset path does not match deployment contract`
  );
  assert(
    (competency.description.match(/<p>/g) ?? []).length === 3,
    `${id}: expected three source-backed description paragraphs`
  );
  assert(
    !Object.prototype.hasOwnProperty.call(CORE_DAGGERHEART_127_DOMAINS, id),
    `${id}: collides with a Daggerheart 1.2.7 core domain`
  );
}

// Verify every one of the 231 domain cards points at one of the registered IDs.
const domainDocs = await sourceDocuments(
  path.join(ROOT, "src", "packs", "system", "domains")
);
const cardCounts = Object.fromEntries(EXPECTED_IDS.map(id => [id, 0]));

for (const { name, doc } of domainDocs) {
  assert(doc.type === "domainCard", `${name}: expected domainCard document`);
  const domain = doc.system?.domain;
  assert(
    Object.prototype.hasOwnProperty.call(cardCounts, domain),
    `${name}: unknown Edgeheart Competency/domain "${domain}"`
  );
  if (Object.prototype.hasOwnProperty.call(cardCounts, domain)) {
    cardCounts[domain] += 1;
  }
}

assert(domainDocs.length === 231, `expected 231 domain cards, got ${domainDocs.length}`);
for (const [id, count] of Object.entries(cardCounts)) {
  assert(count === 21, `${id}: expected 21 cards, got ${count}`);
}

// Verify Step 4 class mappings use the same native IDs.
const classDocs = await sourceDocuments(
  path.join(ROOT, "src", "packs", "system", "classes")
);
assert(classDocs.length === 9, `expected 9 classes, got ${classDocs.length}`);

for (const { name, doc } of classDocs) {
  const key = doc.flags?.edgeheart?.deployment?.logicalKey;
  const expected = EXPECTED_CLASS_DOMAINS[key];
  assert(Boolean(expected), `${name}: unexpected or missing class logical key ${key}`);
  if (expected) {
    assert(
      JSON.stringify(doc.system?.domains) === JSON.stringify(expected),
      `${key}: system.domains ${JSON.stringify(doc.system?.domains)} != ${JSON.stringify(expected)}`
    );
  }
}

// Test deterministic merge behavior outside Foundry.
const unrelatedDomain = {
  id: "custom-domain",
  label: "Custom Domain",
  src: "icons/svg/portal.svg",
  description: "<p>Unrelated homebrew.</p>"
};

const firstPlan = planCompetencyRegistration({
  coreDomains: CORE_DAGGERHEART_127_DOMAINS,
  homebrewDomains: { "custom-domain": unrelatedDomain }
});

assert(firstPlan.added.length === 11, "first registration should add all 11 Competencies");
assert(firstPlan.conflicts.length === 0, "first registration should have no homebrew conflicts");
assert(firstPlan.coreConflicts.length === 0, "first registration should have no core conflicts");
assert(
  firstPlan.nextDomains["custom-domain"]?.label === "Custom Domain",
  "registration must preserve unrelated Homebrew domains"
);

const secondPlan = planCompetencyRegistration({
  coreDomains: CORE_DAGGERHEART_127_DOMAINS,
  homebrewDomains: firstPlan.nextDomains
});

assert(secondPlan.added.length === 0, "second registration must be idempotent");
assert(secondPlan.unchanged.length === 11, "second registration should recognize all 11 unchanged");
assert(secondPlan.changed === false, "second registration must not rewrite world settings");

const conflictingNetwork = {
  ...firstPlan.nextDomains,
  network: {
    id: "network",
    label: "Existing Network",
    src: "icons/svg/portal.svg",
    description: "<p>Existing world-owned data.</p>"
  }
};
const conflictPlan = planCompetencyRegistration({
  coreDomains: CORE_DAGGERHEART_127_DOMAINS,
  homebrewDomains: conflictingNetwork
});

assert(
  conflictPlan.conflicts.map(x => x.id).includes("network"),
  "same-ID differing Homebrew domain must be reported as a conflict"
);
assert(
  conflictPlan.nextDomains.network.label === "Existing Network",
  "same-ID differing Homebrew domain must not be silently overwritten"
);

const coreConflictPlan = planCompetencyRegistration({
  coreDomains: { ...CORE_DAGGERHEART_127_DOMAINS, network: { id: "network" } },
  homebrewDomains: {}
});
assert(
  coreConflictPlan.coreConflicts.includes("network"),
  "core-domain collisions must be rejected"
);
assert(
  !Object.prototype.hasOwnProperty.call(coreConflictPlan.nextDomains, "network"),
  "core-domain collisions must not be inserted into Homebrew domains"
);

// Verify the module entry point actually calls the runtime registrar.
const mainSource = await fs.readFile(path.join(ROOT, "scripts", "main.js"), "utf8");
assert(
  mainSource.includes('from "./competencies.js"'),
  "scripts/main.js must import Competency registration"
);
assert(
  mainSource.includes('Hooks.once("ready"'),
  "Competency registration must run after Daggerheart settings are initialized"
);
assert(
  mainSource.includes("registerEdgeheartCompetencies"),
  "scripts/main.js must invoke registerEdgeheartCompetencies"
);

await fs.mkdir(REPORT_DIR, { recursive: true });

const summary = {
  step: 5,
  status: errors.length ? "FAIL" : "PASS",
  implementation: "Daggerheart 1.2.7 native Homebrew domains",
  competencyCount: ids.length,
  competencyIds: ids,
  domainCardCount: domainDocs.length,
  cardsByCompetency: cardCounts,
  classDomainMappingsValidated: Object.keys(EXPECTED_CLASS_DOMAINS).length,
  idempotentMergeValidated: errors.length === 0,
  unrelatedHomebrewPreservationValidated: errors.length === 0,
  conflictPreservationValidated: errors.length === 0,
  coreCollisionGuardValidated: errors.length === 0,
  runtimeFoundryQualificationPending: true,
  artPathRewritePending: true,
  compendiumCompilationPending: true,
  nextStep: "Rewrite final Edgeheart asset paths after generated art is staged in the module."
};

await fs.writeFile(
  path.join(REPORT_DIR, "step5-summary.json"),
  JSON.stringify(summary, null, 2) + "\n",
  "utf8"
);

const reportLines = [
  "# Edgeheart Foundry Build — Step 5 Report",
  "",
  `**Status:** ${summary.status}`,
  "",
  `- Native Competencies defined: **${ids.length}**`,
  `- Domain cards validated: **${domainDocs.length}**`,
  `- Cards per Competency: **21 each**`,
  `- Class mappings validated: **${summary.classDomainMappingsValidated}**`,
  "- Registration mechanism: **Daggerheart 1.2.7 world-scoped Homebrew domains**",
  "- Idempotent registration behavior: **validated**",
  "- Unrelated Homebrew preservation: **validated**",
  "- Same-ID conflict preservation: **validated**",
  "- Core-domain collision guard: **validated**",
  "- Foundry runtime qualification: **pending downstream runtime test**",
  "- Final art-path rewrite: **pending next deployment step**",
  "- LevelDB Compendium compilation: **pending downstream step**",
  ""
];

if (errors.length) {
  reportLines.push("## Validation errors", "", ...errors.map(error => `- ${error}`), "");
}

await fs.writeFile(
  path.join(REPORT_DIR, "STEP-5-REPORT.md"),
  reportLines.join("\n"),
  "utf8"
);

if (errors.length) {
  console.error("Edgeheart Step 5 Competency registration validation FAILED");
  for (const error of errors) console.error(` - ${error}`);
  process.exit(1);
}

console.log("Edgeheart Step 5 Competency registration validation PASS");
console.log(" - native Competencies: 11");
console.log(" - domain cards: 231 (21 each)");
console.log(" - class domain mappings: 9");
console.log(" - idempotence/conflict/core-collision safeguards: PASS");
