[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/OG2BIT001/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/OG2BIT001/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# THE WORLD TODAY — 21 November 2026 in one image

Entry for the make.fun bounty **news-image-20261121** ("Sum up 21
November's world news in one image", $100).

`main.py` is a Python 3 program (standard library only) that draws a
one-page newspaper front page for **Saturday 21 November 2026** and
writes it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
The PNG is encoded by hand with `zlib` + `struct`; every picture is
drawn in code — rectangles, lines, circles, triangles and a 5×7 bitmap
font defined in the program. No network, no clock, no randomness: two
runs write byte-identical files.

## The day's stories, as drawn

- **Lead — Russia's barrage on Ukraine reaches Poland.** More than
  400 drones and 110 missiles fired overnight; Kyiv hit hardest, at
  least eight killed; two missiles and a suspected drone came down in
  Poland, which called it a deliberate provocation.
- **Markets — AI stock rout.** US stocks fell 3.7% as the AI and chip
  sell-off pushed the S&P 500 and Dow into correction.
- **Justice — ICJ genocide ruling.** The International Court of
  Justice found Myanmar responsible for genocide against the Rohingya,
  in the case brought by The Gambia.
- **Climate — COP31 in overtime.** The UN climate summit in Antalya
  ran past its deadline, nearly 200 nations divided over fossil fuels.
- **Politics — UK–EU reset.** Prime Minister Burnham and EU leaders
  signed post-Brexit agreements on food trade, carbon markets and
  youth mobility in Brussels.
- **Health — cancer pill hope.** In a trial, the pill daraxonrasib
  left pancreatic tumours undetectable on scans in one in 12 patients.
- **Diplomacy — Shenzhen trilateral.** Trump, Xi and Putin concluded
  their summit with a shared peace declaration.
- **In brief —** a tanker hit by an unknown projectile leaving the
  Strait of Hormuz (UKMTO); Saudi air defences downing Houthi missiles
  aimed at Riyadh; Gen Z protests spreading across Europe.

Stories were verified against live reporting of 21 November 2026
(Reuters, AP, France 24, SCMP, The Japan Times and same-day news
digests) before being drawn.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024×1024, ~23 KB)
```

## Licence

MIT — see `LICENSE`. Build notes are in `SESSION.md`.
