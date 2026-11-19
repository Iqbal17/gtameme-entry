# The GTA 6 Bus Stop — a make.fun meme entry

An entry for make.fun's **"Post a GTA 6 meme on X"** bounty
(gta6-meme-x-01, $500 over 50 places). The entry is a public post on
X: its first picture is the meme below, and its text carries
@makefunai, a link to the bounty and the entrant's play code.

make.fun is a site where people and their AI agents build things,
enter them in paid competitions (bounties) and earn real money when
they win.

## The meme

![The GTA 6 bus stop meme](meme.png)

The joke: a fan has waited at a "GTA 6 — ARRIVING: SOON" bus stop
since 2013. The calendar pages of the wait (2013, 2018, 2023, 2026)
litter the sand, his hair has gone grey, and he leans on a cane. The
make.fun ghost — white, black outline, sparkle eyes, holding its
magenta star coin — sat down beside him and, unlike him, got paid
while waiting: *"I GOT PAID ON MAKE.FUN WHILE WE WAITED!"* Thirteen
years later the game is out, and it is still the best day ever.

The picture is original art drawn entirely in code — no game assets,
logos or screenshots. `make_meme.py` (Python, standard library only,
its own tiny bitmap font and PNG writer) draws the 1024×1024
`meme.png`:

```sh
python3 make_meme.py
```

## The program

`main.ts` (Node 22, standard library only) is what the grader runs.
It copies `meme.png` — and `POST.json`, once the entrant has added it
— from the repository root into the output directory, byte for byte.
The output directory is emptied contents-only first (it is a mount
point in the grader; removing the directory itself would fail), so
every run writes identical bytes.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `main.ts` — the entrypoint the grader runs.
- `make_meme.py` — draws the meme; the source of `meme.png`.
- `meme.png` — the meme picture the X post carries (1024×1024).
- `POST_TEXT.md` — the post's draft text, with a `<PLAYCODE>`
  placeholder where the entrant's play code goes.
- `POST.json` — **added by the entrant after posting**: it names the
  post as `{"url": "https://x.com/<handle>/status/<id>"}`. It is
  deliberately absent until the post exists.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
