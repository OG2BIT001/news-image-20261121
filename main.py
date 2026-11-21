#!/usr/bin/env python3
"""THE WORLD TODAY -- one-page newspaper summing up the world news of
Saturday 21 November 2026, drawn entirely in code.

Standard library only. The PNG is encoded by hand (zlib + struct) and
every picture is drawn with the small raster toolkit below: filled
rectangles, lines, circles, triangles and a 5x7 bitmap font defined in
this file. No network, no clock, no randomness: two runs write the
same bytes.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 24, 22)
RED = (176, 32, 32)
DARKRED = (128, 22, 22)
GREY = (96, 91, 82)
FAINT = (214, 207, 188)
BLUE = (36, 72, 132)
SKY = (168, 196, 224)
GOLD = (198, 148, 30)
GREEN = (44, 106, 64)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)

# ---------------------------------------------------------------- canvas
buf = bytearray(PAPER * (W * H))


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]
        buf[i + 1] = c[1]
        buf[i + 2] = c[2]


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, c)


def rect_outline(x, y, w, h, c, t=2):
    rect(x, y, w, t, c)
    rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c)
    rect(x + w - t, y, t, h, c)


def line(x0, y0, x1, y1, c, t=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    r = t // 2
    while True:
        for yy in range(y - r, y - r + t):
            for xx in range(x - r, x - r + t):
                px(xx, yy, c)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def circle(cx, cy, r, c, fill=False):
    if fill:
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    px(xx, yy, c)
    else:
        x, y, err = r, 0, 1 - r
        while x >= y:
            for ox, oy in ((x, y), (y, x), (-y, x), (-x, y),
                           (-x, -y), (-y, -x), (y, -x), (x, -y)):
                px(cx + ox, cy + oy, c)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1


def tri(x0, y0, x1, y1, x2, y2, c):
    minx = max(0, min(x0, x1, x2))
    maxx = min(W - 1, max(x0, x1, x2))
    miny = max(0, min(y0, y1, y2))
    maxy = min(H - 1, max(y0, y1, y2))
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if d == 0:
        return
    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            w0 = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / d
            w1 = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / d
            w2 = 1.0 - w0 - w1
            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                px(xx, yy, c)


# ---------------------------------------------------------------- font
# A 5x7 bitmap font, drawn by hand for this program. Each glyph is
# seven rows of five pixels, '#' for ink and '.' for blank.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    '2': (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '(': ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ')': ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '%': ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#.###"),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '&': (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".#.#."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '*': (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '·': (".....", ".....", ".....", ".##..", ".##..", ".....", "....."),
    '£': (".##..", "#..#.", "#....", "####.", "#....", "#....", "#####"),
}


def text_w(s, scale):
    if not s:
        return 0
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c, bold=False):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[' '])
        for gy, row in enumerate(glyph):
            for gx, cell in enumerate(row):
                if cell == '#':
                    rect(cx + gx * scale, y + gy * scale, scale, scale, c)
                    if bold:
                        rect(cx + gx * scale + max(1, scale // 3),
                             y + gy * scale, scale, scale, c)
        cx += 6 * scale
    return cx - scale - x


def draw_centered(cx, y, s, scale, c, bold=False):
    return draw_text(cx - text_w(s, scale) // 2, y, s, scale, c, bold)


def wrap(s, scale, maxw):
    words = s.upper().split()
    lines = []
    cur = ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_w(trial, scale) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def paragraph(x, y, s, scale, c, maxw, gap=5):
    for ln in wrap(s, scale, maxw):
        draw_text(x, y, ln, scale, c)
        y += 7 * scale + gap
    return y


# ---------------------------------------------------------------- icons
def icon_chart(x, y):
    line(x, y + 40, x + 56, y + 40, INK, 2)
    line(x, y + 4, x, y + 40, INK, 2)
    pts = [(x + 4, y + 10), (x + 16, y + 16), (x + 26, y + 12),
           (x + 38, y + 24), (x + 52, y + 34)]
    for a, b in zip(pts, pts[1:]):
        line(a[0], a[1], b[0], b[1], RED, 3)
    tri(x + 52, y + 40, x + 44, y + 30, x + 58, y + 28, RED)


def icon_scales(x, y):
    rect(x + 26, y + 2, 4, 40, INK)
    rect(x + 18, y + 40, 20, 4, INK)
    line(x + 6, y + 8, x + 50, y + 8, INK, 3)
    for cx in (x + 6, x + 50):
        line(cx, y + 8, cx - 7, y + 24, INK, 2)
        line(cx, y + 8, cx + 7, y + 24, INK, 2)
        line(cx - 9, y + 24, cx + 9, y + 24, INK, 3)
    circle(x + 28, y + 4, 3, GOLD, fill=True)


def icon_sun(x, y):
    circle(x + 28, y + 20, 11, GOLD, fill=True)
    for dx, dy in ((0, -16), (0, 16), (-16, 0), (16, 0), (-11, -11),
                   (11, -11), (-11, 11), (11, 11)):
        line(x + 28 + dx * 2 // 3, y + 20 + dy * 2 // 3,
             x + 28 + dx, y + 20 + dy, GOLD, 3)
    rect(x + 48, y + 6, 5, 30, INK)
    rect(x + 46, y + 34, 9, 4, INK)
    rect(x + 49, y + 12, 3, 20, RED)


def icon_flags(x, y):
    rect(x + 6, y + 2, 3, 42, INK)
    rect(x + 40, y + 2, 3, 42, INK)
    rect(x + 9, y + 3, 22, 15, BLUE)
    line(x + 9, y + 3, x + 31, y + 18, WHITE, 2)
    line(x + 31, y + 3, x + 9, y + 18, WHITE, 2)
    rect(x + 18, y + 3, 4, 15, RED)
    rect(x + 9, y + 9, 22, 4, RED)
    rect(x + 43, y + 3, 22, 15, GOLD)
    circle(x + 54, y + 10, 5, BLUE)
    for i in range(5):
        rect(x + 46 + (i % 3) * 6, y + 5 + (i // 3) * 6, 2, 2, BLUE)


def icon_pill(x, y):
    rect(x + 6, y + 14, 34, 16, RED)
    rect(x + 34, y + 14, 16, 16, WHITE)
    rect_outline(x + 6, y + 14, 44, 16, INK, 2)
    line(x + 34, y + 14, x + 34, y + 30, INK, 2)
    rect(x + 48, y + 6, 5, 22, GREEN)
    rect(x + 40, y + 14, 21, 5, GREEN)


def icon_podiums(x, y):
    for i, hgt in enumerate((20, 30, 14)):
        bx = x + 4 + i * 18
        rect(bx, y + 42 - hgt, 14, hgt, INK)
        line(bx + 7, y + 42 - hgt, bx + 7, y + 42 - hgt - 8, INK, 2)
        circle(bx + 9, y + 42 - hgt - 10, 3, RED, fill=True)


def burst(cx, cy, r, c):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1),
                   (-1, 1), (-1, -1)):
        line(cx + dx * r // 3, cy + dy * r // 3, cx + dx * r,
             cy + dy * r, c, 2)


def lead_art(y_top, y_base):
    # skyline silhouette with bursts and two missile trails
    heights = [20, 32, 14, 38, 24, 44, 17, 35, 27, 44, 20, 32, 15, 39,
               25, 35, 18, 42, 22, 30, 14, 36, 24, 44, 19, 33, 15, 28]
    x = 28
    for hgt in heights:
        rect(x, y_base - hgt, 32, hgt, INK)
        x += 34
    burst(180, y_top + 8, 13, GOLD)
    burst(520, y_top + 2, 16, RED)
    burst(838, y_top + 10, 12, GOLD)
    line(120, y_top - 26, 196, y_top + 4, GREY, 2)
    tri(196, y_top + 4, 186, y_top + 2, 192, y_top - 6, RED)
    line(760, y_top - 30, 700, y_top + 2, GREY, 2)
    tri(700, y_top + 2, 710, y_top + 2, 704, y_top - 8, RED)


# ---------------------------------------------------------------- layout
M = 28            # page margin
CW = W - 2 * M    # content width


def panel(x, y, w, h, kicker, headline, body, icon):
    rect_outline(x, y, w, h, INK, 2)
    draw_text(x + 12, y + 10, kicker, 2, RED, bold=True)
    hy = y + 32
    for ln in headline:
        draw_text(x + 12, hy, ln, 3, INK, bold=True)
        hy += 24
    icon(x + w // 2 - 30, hy + 2)
    paragraph(x + 12, hy + 56, body, 2, INK, w - 24, gap=4)


def build():
    # ---- masthead
    draw_centered(W // 2, 26, "THE WORLD TODAY", 10, INK, bold=True)
    rect(M, 108, CW, 3, INK)
    rect(M, 115, CW, 7, RED)
    draw_text(M, 134, "EST. 2026", 2, GREY)
    draw_centered(W // 2, 130, "SATURDAY, 21 NOVEMBER 2026", 4, INK,
                  bold=True)
    tw = text_w("WORLD EDITION", 2)
    draw_text(W - M - tw, 134, "WORLD EDITION", 2, GREY)
    rect(M, 168, CW, 3, INK)

    # ---- lead story
    draw_text(M, 184, "CONFLICT · KYIV AND WARSAW", 3, RED, bold=True)
    hy = 216
    for ln in ("RUSSIA UNLEASHES 510", "MISSILES AND DRONES ON",
               "UKRAINE; 2 FALL IN POLAND"):
        draw_text(M, hy, ln, 5, INK, bold=True)
        hy += 47
    paragraph(M, 362,
              "KYIV WAS HIT HARDEST: AT LEAST EIGHT PEOPLE KILLED, "
              "BRIDGES AND STATIONS DAMAGED. WARSAW CALLED THE "
              "MISSILES ON POLISH SOIL A DELIBERATE PROVOCATION.",
              2, INK, CW, gap=6)
    lead_art(436, 476)
    rect(M, 484, CW, 3, INK)

    # ---- story panels, row 1
    pw = (CW - 32) // 3
    ph = 218
    y1 = 496
    panel(M, y1, pw, ph, "MARKETS · NEW YORK",
          ("AI STOCK ROUT", "S&P 500 SLIPS", "INTO CORRECTION"),
          "US STOCKS FELL 3.7% AS AI AND CHIP SHARES LED A DEEP "
          "SELLOFF.",
          icon_chart)
    panel(M + pw + 16, y1, pw, ph, "JUSTICE · THE HAGUE",
          ("WORLD COURT:", "MYANMAR GUILTY", "OF GENOCIDE"),
          "THE ICJ RULED FOR THE GAMBIA OVER THE 2017 ROHINGYA "
          "CRACKDOWN.",
          icon_scales)
    panel(M + 2 * (pw + 16), y1, pw, ph, "CLIMATE · ANTALYA",
          ("COP31 TALKS RUN", "INTO OVERTIME ON", "FOSSIL FUELS"),
          "NEARLY 200 NATIONS IN ANTALYA DEADLOCKED OVER FOSSIL "
          "FUELS.",
          icon_sun)

    # ---- story panels, row 2
    y2 = y1 + ph + 12
    panel(M, y2, pw, ph, "POLITICS · BRUSSELS",
          ("BRITAIN AND EU", "SIGN RESET DEAL", "IN BRUSSELS"),
          "FOOD TRADE, CARBON MARKETS AND YOUTH MOBILITY ALL "
          "AGREED.",
          icon_flags)
    panel(M + pw + 16, y2, pw, ph, "HEALTH · LONDON",
          ("PILL ERASES SOME", "PANCREATIC", "CANCER TUMORS"),
          "DARAXONRASIB LEFT TUMORS UNDETECTABLE IN 1 OF 12 "
          "PATIENTS.",
          icon_pill)
    panel(M + 2 * (pw + 16), y2, pw, ph, "DIPLOMACY · SHENZHEN",
          ("TRUMP, XI, PUTIN", "ISSUE JOINT PEACE", "PLEDGE IN CHINA"),
          "IT ENDED WITH A SHARED PLEDGE AGAINST NUCLEAR WAR.",
          icon_podiums)

    # ---- sources line
    draw_centered(W // 2, 950,
                  "SOURCES: REUTERS · AP · FRANCE 24 · SCMP · THE "
                  "JAPAN TIMES", 2, GREY)

    # ---- in-brief band
    rect(0, 966, W, 58, DARKRED)
    draw_centered(W // 2, 974,
                  "IN BRIEF: TANKER HIT BY UNKNOWN PROJECTILE "
                  "LEAVING THE STRAIT OF HORMUZ", 2, WHITE)
    draw_centered(W // 2, 996,
                  "SAUDI AIR DEFENCES DOWN HOUTHI MISSILES · GEN Z "
                  "PROTESTS SPREAD ACROSS EUROPE", 2, WHITE)


# ---------------------------------------------------------------- png out
def png_bytes():
    raw = bytearray()
    row = W * 3
    for yy in range(H):
        raw.append(0)
        raw += buf[yy * row:(yy + 1) * row]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    build()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(png_bytes())


if __name__ == "__main__":
    main()
