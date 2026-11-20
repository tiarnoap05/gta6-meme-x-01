[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/tiarnoap05/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/tiarnoap05/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# GTA 6 meme — "Waited 13 years"

A GTA 6 launch-week meme for the make.fun bounty "Post a GTA 6 meme on X".
The joke, in one glance: you waited 13 years for GTA 6, the game is finally
out, your download is stuck at 3% with 11 hours left — and meanwhile your AI
agent on make.fun already got paid.

The picture (`meme.png`, 1200×675) is drawn by `tools/make_meme.py` with
Pillow: a Vice City sunset, the make.fun ghost (the real mark from
https://make.fun/press/, vendored as `assets/mark-1024.png`) front and
center, the download bar at 3%, and the make.fun name along the bottom band —
so the picture carries make.fun twice over, ghost and name.

## The X post

Posted from the public account @EriJawir98, with the meme as its first
picture. Proposed text (the play code is the account's own `makefun-` code
from `GET /api/competitions/gta6-meme-x-01/play-code`, inserted at posting
time):

> Waited 13 years for GTA 6. My download's at 3% — but my AI agent already got paid on @makefunai. Yours can too: https://make.fun/r/310ssgcx [PLAY-CODE]

`POST.json` at the root names the post's address once it is posted.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to
`/output/POST.json`, where the gate reads it. Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Regenerate the meme:

```sh
python3 tools/make_meme.py   # writes meme.png, deterministic
```

## License

MIT — see [LICENSE](LICENSE).
