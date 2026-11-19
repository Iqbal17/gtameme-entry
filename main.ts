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

// The meme that the post carries; the program ships it and reproduces
// it into the output directory unchanged.
copyFileSync(join(BOT_DIR, 'meme.png'), join(OUTPUT_DIR, 'meme.png'));

// The post's address, once the entrant has filled POST.json in.
const postFile = join(BOT_DIR, 'POST.json');
if (existsSync(postFile)) {
  copyFileSync(postFile, join(OUTPUT_DIR, 'POST.json'));
}
