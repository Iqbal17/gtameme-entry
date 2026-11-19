// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: the house reads POST.json from this
// repository, reads the post on X, and judges its first picture (the
// meme in meme.png, drawn by make_meme.py) and its text. This program's
// job at grade time is to hand the house its inputs: it copies
// POST.json and meme.png from the repository root into the output
// directory, byte for byte, and prints nothing on success.
//
// POST.json is added by the entrant once the post exists, so a missing
// POST.json is not an error here: the meme copy still runs, and when
// POST.json is present it is copied exactly.
//
// The grader's output directory is a mounted volume: it is created if
// needed and emptied by removing its CONTENTS only. The directory
// itself is never removed (removing a mount point throws EBUSY and
// fails the run).
//
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in
// for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Create the output directory if needed, then empty only its contents
// so a re-run writes exactly the same bytes as a first run.
mkdirSync(OUTPUT_DIR, { recursive: true });
for (const name of readdirSync(OUTPUT_DIR)) {
  rmSync(join(OUTPUT_DIR, name), { recursive: true, force: true });
}

// Deliver one repository file into the output directory. A required
// file that cannot be copied fails the run with a clear message; an
// optional one (POST.json before the post exists) is skipped quietly.
function deliver(name: string, required: boolean): void {
  const from = join(BOT_DIR, name);
  if (!existsSync(from)) {
    if (required) {
      console.error(`${name} is missing from ${BOT_DIR}`);
      process.exit(1);
    }
    return;
  }
  copyFileSync(from, join(OUTPUT_DIR, name));
}

// The meme that the post carries; the program ships it and reproduces
// it into the output directory unchanged.
deliver('meme.png', true);

// The post's address, once the entrant has filled POST.json in.
deliver('POST.json', false);
