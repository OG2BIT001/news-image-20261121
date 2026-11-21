#!/usr/bin/env python3
"""Draw the entry artwork for news-image-20261121: a newspaper front page
summing up Saturday 21 November 2026. All art is drawn here with PIL
primitives -- no third-party images, logos or likenesses. Output: entry.png
(1024x1024). Deterministic: same pixels every run.

Design follows the sibling entry news-image-20261120 (same front-page
system, new stories and motifs)."""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36                      # page margin
CW = W - 2 * M              # content width = 952

PAPER = (250, 246, 236)
INK = (22, 24, 28)
GREY = (84, 84, 88)
RED = (178, 32, 42)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
BODY = (40, 42, 48)

F = "/usr/share/fonts/truetype/noto/"
L = "/usr/share/fonts/truetype/liberation/"
D = "/usr/share/fonts/truetype/dejavu/"
SERIF_BLACK = F + "NotoSerif-Black.ttf"
SANS_BLACK = F + "NotoSans-Black.ttf"
SANS_XBOLD = F + "NotoSans-ExtraBold.ttf"
SANS_BOLD = F + "NotoSans-Bold.ttf"
SANS = F + "NotoSans-Regular.ttf"
SERIF_IT = L + "LiberationSerif-Italic.ttf"
DEJAVU_BOLD = D + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, cx, y, text, fnt, fill, tracking=6):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, maxw, lh):
    lines = wrap(draw, text, fnt, maxw)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return len(lines) * lh


# ---------------------------------------------------------------- motifs
def motif_climate(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 92, 80))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 172, 205))
    green = (52, 140, 74)
    d.pieslice([cx - 28, cy - 32, cx + 4, cy - 2], 200, 330, fill=green)
    d.pieslice([cx + 2, cy - 6, cx + 34, cy + 26], 90, 250, fill=green)
    d.pieslice([cx - 32, cy + 8, cx - 2, cy + 36], 300, 90, fill=green)
    d.arc([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], start=290, end=60,
          fill=(255, 120, 60), width=5)


def motif_kyiv(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 60, 88))
    base = y1 - 10
    sil = (18, 20, 30)
    d.rectangle([x0 + 6, base - 46, x0 + 32, base], fill=sil)
    d.rectangle([x1 - 32, base - 38, x1 - 6, base], fill=sil)
    cx = (x0 + x1) // 2
    d.rectangle([cx - 26, base - 56, cx + 26, base], fill=sil)
    d.pieslice([cx - 26, base - 100, cx + 26, base - 46], 180, 360, fill=(201, 146, 42))
    d.polygon([(cx - 4, base - 98), (cx + 4, base - 98), (cx, base - 122)], fill=(201, 146, 42))
    d.line([cx, base - 122, cx, base - 134], fill=(201, 146, 42), width=3)
    d.line([cx - 5, base - 129, cx + 5, base - 129], fill=(201, 146, 42), width=3)
    for wx in (x0 + 13, cx - 14, cx + 10, x1 - 24):
        d.rectangle([wx, base - 20, wx + 4, base - 14], fill=(240, 210, 120))


def motif_magnifier(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(27, 58, 99))
    cx, cy = (x0 + x1) // 2 - 8, (y0 + y1) // 2 - 14
    r = 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=8)
    d.line([cx + 28, cy + 28, cx + 52, cy + 52], fill=WHITE, width=10)
    f = font(SANS_BLACK, 52)
    tw = d.textlength("?", font=f)
    d.text((cx - tw / 2, cy - 30), "?", font=f, fill=(255, 210, 60))
    d.line([x0 + 14, y1 - 30, x1 - 14, y1 - 30], fill=(255, 210, 60), width=4)


def motif_barrier(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(22, 30, 46))
    cy = (y0 + y1) // 2
    # two posts and a red-white striped barrier bar
    d.rectangle([x0 + 14, cy - 52, x0 + 24, cy + 52], fill=(196, 206, 220))
    d.rectangle([x1 - 24, cy - 52, x1 - 14, cy + 52], fill=(196, 206, 220))
    bx0, bx1, by0, by1 = x0 + 14, x1 - 14, cy - 14, cy + 14
    d.rectangle([bx0, by0, bx1, by1], fill=WHITE)
    for sx in range(bx0 - 28, bx1, 28):
        d.polygon([(sx, by1), (sx + 14, by1), (sx + 28, by0), (sx + 14, by0)],
                  fill=RED)
    d.line([x0 + 10, y1 - 18, x1 - 10, y1 - 18], fill=(255, 210, 60), width=4)


def motif_hospital(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(243, 236, 216))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], fill=(14, 120, 110))
    d.rectangle([cx - 12, cy - 32, cx + 12, cy + 32], fill=WHITE)
    d.rectangle([cx - 32, cy - 12, cx + 32, cy + 12], fill=WHITE)


def motif_maths(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(38, 44, 62))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    f = font(DEJAVU_BOLD, 44)
    tw = d.textlength("\u03c0", font=f)
    d.text((cx - tw / 2, cy - 24), "\u03c0", font=f, fill=(255, 210, 60))


def motif_scales(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(243, 236, 216))
    cx = (x0 + x1) // 2
    top = y0 + 40
    gold = (176, 132, 38)
    d.line([x0 + 30, top, x1 - 30, top], fill=INK, width=6)
    d.line([cx, top, cx, y1 - 44], fill=INK, width=6)
    d.ellipse([cx - 8, top - 14, cx + 8, top + 2], fill=gold)
    for px in (x0 + 30, x1 - 30):
        py = top + 40
        d.line([px, top, px - 20, py], fill=INK, width=3)
        d.line([px, top, px + 20, py], fill=INK, width=3)
        d.line([px - 22, py, px + 22, py], fill=INK, width=4)
        d.arc([px - 22, py - 9, px + 22, py + 17], start=0, end=180, fill=INK, width=4)
    d.rectangle([cx - 30, y1 - 40, cx + 30, y1 - 30], fill=INK)
    d.rectangle([cx - 17, y1 - 48, cx + 17, y1 - 40], fill=gold)


# ---------------------------------------------------------------- panels
def panel(d, box, motif, kicker, headline, summary):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PANEL, outline=INK, width=2)
    motif(d, (x0, y0, x0 + 118, y1))
    tx = x0 + 134
    tw = x1 - tx - 14
    d.text((tx, y0 + 11), kicker, font=font(SANS_BOLD, 19), fill=RED)
    hh = text_block(d, tx, y0 + 38, headline, font(SANS_BLACK, 26), INK, tw, 32)
    text_block(d, tx, y0 + 44 + hh, summary, font(SANS, 20), BODY, tw, 26)


def half_panel(d, box, motif, kicker, headline, summary):
    x0, y0, x1, y1 = box
    motif(d, (x0, y0, x0 + 54, y1))
    tx = x0 + 66
    tw = x1 - tx - 10
    d.text((tx, y0 + 8), kicker, font=font(SANS_BOLD, 17), fill=RED)
    hh = text_block(d, tx, y0 + 30, headline, font(SANS_XBOLD, 23), INK, tw, 28)
    text_block(d, tx, y0 + 34 + hh, summary, font(SANS, 18), BODY, tw, 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    tracked(d, W // 2, 18, "THE WORLD'S NEWS IN ONE PICTURE", font(SANS_BOLD, 24), INK, 7)
    d.line([M, 50, W - M, 50], fill=INK, width=3)
    date_f = font(SERIF_BLACK, 88)
    dtxt = "21 NOVEMBER 2026"
    tw = d.textlength(dtxt, font=date_f)
    d.text(((W - tw) / 2, 56), dtxt, font=date_f, fill=INK)
    sub = "SATURDAY — seven stories that defined the day: climate, war, espionage, security, politics, science and justice"
    sub_f = font(SERIF_IT, 21)
    tw = d.textlength(sub, font=sub_f)
    d.text(((W - tw) / 2, 152), sub, font=sub_f, fill=GREY)
    d.line([M, 184, W - M, 184], fill=INK, width=5)

    # lead panel — COP31 overtime
    box = (M, 196, W - M, 412)
    d.rectangle(box, fill=PANEL, outline=INK, width=2)
    motif_climate(d, (M, 196, M + 196, 412))
    tx = M + 220
    tw = W - M - tx - 18
    d.text((tx, 212), "CLIMATE · ANTALYA, TURKEY", font=font(SANS_BOLD, 21), fill=RED)
    hh = text_block(d, tx, 242, "COP31 SPILLS INTO OVERTIME",
                    font(SANS_BLACK, 42), INK, tw, 50)
    text_block(d, tx, 252 + hh,
               "Negotiators miss their Friday deadline as the draft deal drops "
               "all mention of fossil fuels; a third text is promised for Saturday.",
               font(SANS, 25), BODY, tw, 34)

    # row A — Ukraine barrage | Denmark expulsion
    panel(d, (M, 424, M + 470, 634), motif_kyiv, "WAR · KYIV, UKRAINE",
          "RUSSIA'S BIGGEST BARRAGE HITS KYIV",
          "Missiles and drones kill nine and knock out three Dnipro bridges; a missile lands in Poland.")
    panel(d, (W - M - 470, 424, W - M, 634), motif_magnifier, "ESPIONAGE · COPENHAGEN",
          "DENMARK EXPELS RUSSIAN DIPLOMAT",
          "Intelligence says Moscow plotted to kill rapper Kyivstoner; the attaché has seven days to leave.")

    # row B — Estonia border | Bolsonaro
    panel(d, (M, 646, M + 470, 856), motif_barrier, "SECURITY · TALLINN, ESTONIA",
          "ESTONIA SHUTS ITS BORDER WITH RUSSIA",
          "All road crossings close for six months from 1 December after alleged arson; Moscow warns of a \u201cnew Iron Curtain\u201d.")
    panel(d, (W - M - 470, 646, W - M, 856), motif_hospital, "POLITICS · BRASÍLIA, BRAZIL",
          "BOLSONARO BACK IN HOSPITAL",
          "The jailed ex-president, 71, is treated for a near-complete intestinal obstruction; doctors say he is stable.")

    # row C — Riemann | Gupta, one wide band with a centre divider
    band = (M, 868, W - M, 1006)
    d.rectangle(band, fill=PANEL, outline=INK, width=2)
    d.line([W // 2, 868, W // 2, 1006], fill=INK, width=2)
    half_panel(d, (M, 868, W // 2, 1006), motif_maths, "SCIENCE · ARTIFICIAL INTELLIGENCE",
               "CLAUDE 'PROVES' MATHS' GREATEST RIDDLE",
               "An Anthropic researcher says its chatbot proved the Riemann Hypothesis.")
    half_panel(d, (W // 2, 868, W - M, 1006), motif_scales, "JUSTICE · NEW YORK, USA",
               "US JAILS MAN FOR 19 YEARS OVER SIKH MURDER PLOT",
               "Nikhil Gupta is sentenced for a murder-for-hire plot against a Sikh separatist.")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
