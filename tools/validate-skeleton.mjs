import { promises as fs } from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const manifest = JSON.parse(await fs.readFile(path.join(ROOT, "module.json"), "utf8"));
const errors = [];

function assert(condition, message) {
  if (!condition) errors.push(message);
}

assert(manifest.id === "edgeheart", 'module id must be "edgeheart"');
assert(manifest.compatibility?.minimum === "14.368", "Foundry minimum must target 14.368");
assert(manifest.compatibility?.verified === "14.368", "Foundry verified version must target 14.368");
assert(manifest.compatibility?.maximum === "14", "Foundry maximum must remain generation 14");

const dh = manifest.relationships?.systems?.find((s) => s.id === "daggerheart");
assert(Boolean(dh), "Daggerheart system relationship is required");
assert(dh?.compatibility?.minimum === "2.10.5", "Daggerheart minimum must target 2.10.5");
assert(dh?.compatibility?.verified === "2.10.5", "Daggerheart verified version must target 2.10.5");
assert(dh?.compatibility?.maximum === undefined, "Daggerheart maximum must remain unset so 2.10.x patches are not hard-blocked");

const packs = manifest.packs ?? [];
const packNames = packs.map((p) => p.name);
assert(new Set(packNames).size === packNames.length, "Compendium pack names must be unique");

const packPaths = packs.map((p) => p.path);
assert(new Set(packPaths).size === packPaths.length, "Compendium pack paths must be unique");

for (const pack of packs) {
  assert(pack.path.endsWith(".db"), `pack path must end in .db: ${pack.path}`);
  const compiledRel = pack.path.slice(0, -3);
  const sourceDir = path.join(ROOT, "src", compiledRel);
  try {
    const stat = await fs.stat(sourceDir);
    assert(stat.isDirectory(), `source pack path must be a directory: src/${compiledRel}`);
  } catch {
    errors.push(`missing source pack directory: src/${compiledRel}`);
  }
}

function visitFolder(folder) {
  for (const packName of folder.packs ?? []) {
    assert(packNames.includes(packName), `packFolders references unknown pack: ${packName}`);
  }
  for (const child of folder.folders ?? []) visitFolder(child);
}
for (const folder of manifest.packFolders ?? []) visitFolder(folder);

if (errors.length) {
  console.error("Edgeheart skeleton validation FAILED");
  for (const err of errors) console.error(` - ${err}`);
  process.exit(1);
}

console.log(`Edgeheart skeleton validation PASS (${packs.length} Compendia declared)`);
