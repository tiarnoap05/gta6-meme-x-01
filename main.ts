// gta6-meme-x-01 entry (Node 22, standard library only): copy POST.json from
// the repository root to /output/POST.json, where the gate reads it. That is
// all the program has to do. The entry is the post itself: the meme is posted
// on X from a public account with make.fun (a link or written out) and/or a
// tag of @makefunai and the entrant's play code in its text, POST.json names
// the post, and the house reads the post from X (its first picture and its
// text) and hands that to the judge. Nothing this program writes about the
// post is judged.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Fail fast with a clear message when POST.json is not the shape the gate
// needs, instead of copying a broken file that the gate would refuse.
const postPath = join(BOT_DIR, "POST.json");
let post: unknown;
try {
  post = JSON.parse(readFileSync(postPath, "utf8"));
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== "object" || post === null || typeof (post as { url?: unknown }).url !== "string") {
  console.error(`POST.json in ${BOT_DIR} has no string "url" field; the gate needs {"url": "https://x.com/<handle>/status/<id>"}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(postPath, join(OUTPUT_DIR, "POST.json"));
} catch (err) {
  console.error(
    `POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`,
  );
  process.exit(1);
}
