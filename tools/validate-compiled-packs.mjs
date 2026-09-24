#!/usr/bin/env node

/**
 * Step 7 compiled-pack validation.
 *
 * Compiles are derivative outputs. This validator proves that every declared
 * Edgeheart Compendium:
 * - exists as a LevelDB pack;
 * - can be extracted by Foundry's official CLI;
 * - contains the same stable document/folder identities as src/packs;
 * - preserves expected document type/name/folder relationships.
 *
 * Runtime sheet/application qualification remains a later clean-world test.
 */

import { extractPack } from "@foundryvtt/foundryvtt-cli";
import { promises as fs } from "node:fs";
import path from "node:path";
import os from "node:os";

const ROOT = process.cwd();
const manifest = JSON.parse(
  await fs.readFile(path.join(ROOT, "module.json"), "utf8")
);

const EXPECTED_TOTAL_SOURCE_ENTRIES = 810;
const EXPECTED_PACK_ENTRY_COUNTS = {
  "edgeheart-weapons": 68,
  "edgeheart-armors": 29,
  "edgeheart-loot": 40,
  "edgeheart-consumables": 40,
  "edgeheart-cyberware": 60,
  "edgeheart-classes": 9,
  "edgeheart-subclasses": 18,
  "edgeheart-domains": 352,
  "edgeheart-features": 143,
  "edgeheart-ancestries": 6,
  "edgeheart-communities": 8,
  "edgeheart-adversaries": 22,
  "edgeheart-environments": 15
};

const errors = [];
const results = [];

const stripDb = packPath =>
  packPath.endsWith(".db") ? packPath.slice(0, -3) : packPath;

async function readJsonDocuments(directory) {
  const result = new Map();
  const entries = await fs.readdir(directory);
  for (const name of entries.sort()) {
    if (!name.toLowerCase().endsWith(".json")) continue;
    const doc = JSON.parse(
      await fs.readFile(path.join(directory, name), "utf8")
    );
    if (!doc._id) {
      errors.push(`${directory}/${name}: missing _id`);
      continue;
    }
    if (result.has(doc._id)) {
      errors.push(`${directory}: duplicate _id ${doc._id}`);
      continue;
    }
    result.set(doc._id, doc);
  }
  return result;
}

function comparable(doc) {
  return {
    _id: doc._id ?? null,
    _key: doc._key ?? null,
    name: doc.name ?? null,
    type: doc.type ?? null,
    folder: doc.folder ?? null
  };
}

function compareIdentity(source, extracted, context) {
  const a = comparable(source);
  const b = comparable(extracted);
  for (const key of Object.keys(a)) {
    if (a[key] !== b[key]) {
      errors.push(
        `${context}: ${key} mismatch; source=${JSON.stringify(a[key])} extracted=${JSON.stringify(b[key])}`
      );
    }
  }
}

const tempRoot = await fs.mkdtemp(
  path.join(os.tmpdir(), "edgeheart-pack-validation-")
);

try {
  let totalSource = 0;
  let totalExtracted = 0;

  for (const pack of manifest.packs ?? []) {
    const compiledRel = stripDb(pack.path);
    const compiledAbs = path.join(ROOT, compiledRel);
    const sourceAbs = path.join(ROOT, "src", compiledRel);
    const expectedCount = EXPECTED_PACK_ENTRY_COUNTS[pack.name];

    if (expectedCount === undefined) {
      errors.push(`No expected count declared for pack ${pack.name}`);
      continue;
    }

    try {
      const stat = await fs.stat(compiledAbs);
      if (!stat.isDirectory()) {
        errors.push(`${pack.name}: compiled pack is not a directory: ${compiledRel}`);
        continue;
      }
    } catch {
      errors.push(`${pack.name}: compiled pack missing: ${compiledRel}`);
      continue;
    }

    const levelFiles = await fs.readdir(compiledAbs);
    if (levelFiles.length === 0) {
      errors.push(`${pack.name}: compiled LevelDB directory is empty`);
      continue;
    }

    const sourceDocs = await readJsonDocuments(sourceAbs);
    totalSource += sourceDocs.size;

    if (sourceDocs.size !== expectedCount) {
      errors.push(
        `${pack.name}: expected ${expectedCount} source entries, got ${sourceDocs.size}`
      );
    }

    const extractDir = path.join(tempRoot, pack.name);
    await fs.mkdir(extractDir, { recursive: true });

    await extractPack(compiledAbs, extractDir, {
      yaml: false,
      transformName: doc => `${doc._id}.json`
    });

    const extractedDocs = await readJsonDocuments(extractDir);
    totalExtracted += extractedDocs.size;

    if (extractedDocs.size !== sourceDocs.size) {
      errors.push(
        `${pack.name}: extracted count ${extractedDocs.size} != source count ${sourceDocs.size}`
      );
    }

    const sourceIds = [...sourceDocs.keys()].sort();
    const extractedIds = [...extractedDocs.keys()].sort();
    if (JSON.stringify(sourceIds) !== JSON.stringify(extractedIds)) {
      const sourceSet = new Set(sourceIds);
      const extractedSet = new Set(extractedIds);
      const missing = sourceIds.filter(id => !extractedSet.has(id)).slice(0, 10);
      const extra = extractedIds.filter(id => !sourceSet.has(id)).slice(0, 10);
      errors.push(
        `${pack.name}: stable-ID set mismatch; missing=${JSON.stringify(missing)} extra=${JSON.stringify(extra)}`
      );
    }

    for (const id of sourceIds) {
      const extracted = extractedDocs.get(id);
      if (!extracted) continue;
      compareIdentity(
        sourceDocs.get(id),
        extracted,
        `${pack.name}/${id}`
      );
    }

    results.push({
      packName: pack.name,
      documentType: pack.type,
      sourcePath: path.relative(ROOT, sourceAbs).replaceAll("\\", "/"),
      compiledPath: compiledRel.replaceAll("\\", "/"),
      sourceEntryCount: sourceDocs.size,
      extractedEntryCount: extractedDocs.size,
      levelDbFileCount: levelFiles.length
    });
  }

  if (totalSource !== EXPECTED_TOTAL_SOURCE_ENTRIES) {
    errors.push(
      `total source entries expected ${EXPECTED_TOTAL_SOURCE_ENTRIES}, got ${totalSource}`
    );
  }
  if (totalExtracted !== EXPECTED_TOTAL_SOURCE_ENTRIES) {
    errors.push(
      `total extracted entries expected ${EXPECTED_TOTAL_SOURCE_ENTRIES}, got ${totalExtracted}`
    );
  }

  const reportDir = path.join(ROOT, "build", "step7");
  await fs.mkdir(reportDir, { recursive: true });

  const summary = {
    step: 7,
    status: errors.length ? "FAIL" : "PASS",
    compiler: "@foundryvtt/foundryvtt-cli",
    declaredCompendiumCount: (manifest.packs ?? []).length,
    totalSourceEntries: totalSource,
    totalExtractedEntries: totalExtracted,
    expectedTotalEntries: EXPECTED_TOTAL_SOURCE_ENTRIES,
    packResults: results,
    foundryRuntimeQualificationPending: true,
    generatedPacksAreDerivative: true,
    nextStep: "Install the built Edgeheart module into a clean Foundry 14.368 / Daggerheart 2.10.5 world and perform runtime qualification."
  };

  await fs.writeFile(
    path.join(reportDir, "step7-summary.json"),
    JSON.stringify(summary, null, 2) + "\n",
    "utf8"
  );

  const lines = [
    "# Edgeheart Foundry Build — Step 7 Compendium Compilation Report",
    "",
    `**Status:** ${summary.status}`,
    "",
    `- Declared Compendia: **${summary.declaredCompendiumCount}**`,
    `- Source entries: **${totalSource}**`,
    `- Successfully re-extracted compiled entries: **${totalExtracted}**`,
    `- Expected entries: **${EXPECTED_TOTAL_SOURCE_ENTRIES}**`,
    "",
    "Each compiled LevelDB pack was re-extracted through the official Foundry CLI",
    "and checked against the stable source document/folder identity set.",
    "",
    "Runtime sheet/application qualification remains pending.",
    ""
  ];

  if (errors.length) {
    lines.push("## Errors", "", ...errors.map(error => `- ${error}`), "");
  }

  await fs.writeFile(
    path.join(reportDir, "STEP-7-REPORT.md"),
    lines.join("\n"),
    "utf8"
  );

  if (errors.length) {
    console.error("Edgeheart Step 7 compiled-pack validation FAILED");
    for (const error of errors) console.error(` - ${error}`);
    process.exit(1);
  }

  console.log("Edgeheart Step 7 compiled-pack validation PASS");
  console.log(` - Compendia: ${summary.declaredCompendiumCount}`);
  console.log(` - Source entries: ${totalSource}`);
  console.log(` - Re-extracted compiled entries: ${totalExtracted}`);
} finally {
  await fs.rm(tempRoot, { recursive: true, force: true });
}
