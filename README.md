[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/OG2BIT001/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/OG2BIT001/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# One image: the world news of Saturday 21 November 2026

Entry for make.fun's [news-image-20261121](https://make.fun/bounty/news-image-20261121)
bounty ("Sum up 21 November's world news in one image", $100). The image is a
newspaper front page, drawn programmatically with PIL: a masthead, the date set
very large, and seven verified stories of the day.

## The seven stories

1. **COP31 spills into overtime** (Antalya, Turkey) — negotiators miss their Friday
   deadline; the draft deal drops all mention of fossil fuels; a third text is
   promised for Saturday. Sources: Reuters, UN News, Al Jazeera, Dawn.
2. **Russia's biggest barrage hits Kyiv** (Ukraine) — overnight missile and drone
   attack kills nine, knocks out three Dnipro bridges; a missile lands in Poland.
   Sources: Kyiv Independent, ANews/AFP, APA.
3. **Denmark expels Russian diplomat** (Copenhagen) — intelligence says Moscow
   plotted to kill Ukrainian-American rapper Kyivstoner; the defence attaché has
   seven days to leave. Sources: Al Jazeera, Kyiv Independent, WSJ, CNN.
4. **Estonia shuts its border with Russia** (Tallinn) — all road crossings close
   for six months from 1 December after alleged arson; Moscow warns of a "new
   Iron Curtain". Sources: Reuters, Al Jazeera, The Hindu.
5. **Bolsonaro back in hospital** (Brasília, Brazil) — the jailed ex-president, 71,
   is treated for a near-complete intestinal obstruction; doctors say he is
   stable. Sources: Reuters, CNN, The Straits Times.
6. **Claude 'proves' maths' greatest riddle** (AI / science) — an Anthropic
   researcher says its chatbot proved the Riemann Hypothesis; the claim awaits
   independent checking. Source: The Hindu (21 Nov digest; first reported 20 Nov).
7. **US jails man for 19 years over Sikh murder plot** (New York, USA) — Nikhil
   Gupta is sentenced for a murder-for-hire plot against a Sikh separatist
   leader. Sources: The Hindu, The Manila Times.

Every story was verified against live reporting on 21 November 2026; see
SESSION.md for the source list and the one date caveat (story 6 was first
reported on 20 November and is worded as a claim, not a settled fact).

## How to run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Copies `entry.png` (1024×1024, 143 KB) to the output directory. Two runs
write byte-identical files (verified: same SHA-256).

## Files

- `main.py` — the entry program (Python 3.13, standard library only)
- `entry.png` — the image
- `build_art.py` — the program that drew the image (PIL, deterministic)
- `SESSION.md` — who built this, how, and the verification log

MIT licensed — see `LICENSE`.
