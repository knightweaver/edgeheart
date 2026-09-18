import { extractPack } from "@foundryvtt/foundryvtt-cli";
import { promises as fs } from "node:fs";
import path from "node:path";
import readline from "node:readline/promises";

const ROOT = process.cwd();
const manifest = JSON.parse(await fs.readFile(path.join(ROOT, "module.json"), "utf8"));
const stripDb = (packPath) => packPath.endsWith(".db") ? packPath.slice(0, -3) : packPath;

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const answer = await rl.question(
  'This will overwrite JSON sources from compiled packs. Type "Overwrite" to continue: '
);
rl.close();

if (answer.toLowerCase() !== "overwrite") {
  console.log("Edgeheart | extraction canceled");
  process.exit(0);
}

function transformName(doc) {
  const safeFileName = (doc.name ?? "unnamed").replace(/[^a-zA-Z0-9А-я]/g, "_");
  const keyType = doc._key?.split("!")[1];
  const prefix = ["actors", "items"].includes(keyType) ? doc.type : keyType ?? "document";
  return `${prefix}_${safeFileName}_${doc._id}.json`;
}

for (const pack of manifest.packs ?? []) {
  const compiledRel = stripDb(pack.path);
  const compiledAbs = path.join(ROOT, compiledRel);
  const sourceRel = path.join("src", compiledRel);
  const sourceAbs = path.join(ROOT, sourceRel);

  try {
    await fs.access(compiledAbs);
  } catch {
    console.warn(`Edgeheart | skipping missing compiled pack: ${compiledRel}`);
    continue;
  }

  await fs.mkdir(sourceAbs, { recursive: true });

  for (const file of await fs.readdir(sourceAbs)) {
    if (file.toLowerCase().endsWith(".json")) {
      await fs.unlink(path.join(sourceAbs, file));
    }
  }

  console.log(`Edgeheart | extracting ${compiledRel} -> ${sourceRel}`);
  await extractPack(compiledAbs, sourceAbs, { yaml: false, transformName });
}
