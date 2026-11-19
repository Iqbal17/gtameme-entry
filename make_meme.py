#!/usr/bin/env python3
"""make_meme.py - draws meme.png for the gta6-meme-x-01 entry.

Original art only, drawn entirely in code with the Python standard
library (no Pillow, no game assets, no logos, no screenshots).
The picture: a Vice City style sunset, a "GTA 6" bus stop that has
said SOON for thirteen years, one very patient fan on a bench, and
the make.fun ghost next to him holding its magenta star coin.

Run:  python3 make_meme.py   ->   writes meme.png (1024x1024)
"""

import math
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- canvas

buf = bytearray(W * H * 3)


def px(x, y, rgb):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = rgb[0]
        buf[i + 1] = rgb[1]
        buf[i + 2] = rgb[2]


def rect(x0, y0, x1, y1, rgb):
    for y in range(max(0, y0), min(H, y1)):
        row = (y * W + x0) * 3
        for x in range(max(0, x0), min(W, x1)):
            i = (y * W + x) * 3
            buf[i] = rgb[0]
            buf[i + 1] = rgb[1]
            buf[i + 2] = rgb[2]
        del row


def circle(cx, cy, r, rgb):
    for y in range(cy - r, cy + r + 1):
        if 0 <= y < H:
            dx = int(math.sqrt(max(0, r * r - (y - cy) * (y - cy))))
            for x in range(cx - dx, cx + dx + 1):
                px(x, y, rgb)


def line(x0, y0, x1, y1, rgb, thick=3):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    rad = thick // 2
    for s in range(steps + 1):
        x = x0 + (x1 - x0) * s // steps
        y = y0 + (y1 - y0) * s // steps
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                px(x + dx, y + dy, rgb)


def poly(points, rgb):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        nodes = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                nodes.append(int(x0 + (y - y0) * (x1 - x0) / (y1 - y0)))
        nodes.sort()
        for i in range(0, len(nodes) - 1, 2):
            for x in range(nodes[i], nodes[i + 1] + 1):
                px(x, y, rgb)


def star(cx, cy, r, rgb, points=5):
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((int(cx + rad * math.cos(ang)), int(cy + rad * math.sin(ang))))
    poly(pts, rgb)


def sparkle(cx, cy, r, rgb):
    pts = [
        (cx, cy - r), (cx + r // 4, cy - r // 4), (cx + r, cy),
        (cx + r // 4, cy + r // 4), (cx, cy + r), (cx - r // 4, cy + r // 4),
        (cx - r, cy), (cx - r // 4, cy - r // 4),
    ]
    poly(pts, rgb)


# ---------------------------------------------------------------- font
# A tiny 5x7 bitmap font, drawn by hand for this entry.

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "01111", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, rgb):
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    rect(cx + gx * scale, y + gy * scale,
                         cx + (gx + 1) * scale, y + (gy + 1) * scale, rgb)
        cx += 6 * scale
    return cx


def text_center(y, s, scale, rgb, cx=W // 2):
    draw_text(cx - text_w(s, scale) // 2, y, s, scale, rgb)


# ---------------------------------------------------------------- scene

BLACK = (10, 10, 14)
WHITE = (255, 255, 255)
YELLOW = (255, 213, 74)
MAGENTA = (236, 0, 140)
DARK = (35, 24, 54)

# sunset gradient sky, down to the sea line
top = (43, 16, 85)
mid = (199, 62, 140)
low = (255, 140, 66)
for y in range(0, 700):
    if y < 350:
        t = y / 350
        c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
    else:
        t = (y - 350) / 350
        c = tuple(int(mid[i] + (low[i] - mid[i]) * t) for i in range(3))
    rect(0, y, W, y + 1, c)

# retro sun with stripe cuts
circle(512, 690, 170, (255, 205, 80))
for i, sy in enumerate((640, 668, 692)):
    rect(300, sy, 724, sy + 6 + i * 3, (255, 150, 80))

# sea and sand
rect(0, 700, W, 792, (18, 130, 160))
for sx in range(60, 1000, 90):
    line(sx, 730 + (sx % 3) * 14, sx + 34, 730 + (sx % 3) * 14, (120, 220, 230), 4)
rect(0, 792, W, 876, (243, 214, 150))

# palm trees, left and right silhouettes
def palm(bx, by, flip=1):
    for s in range(0, 130, 6):
        x = bx + flip * int(22 * math.sin(s / 130 * 1.2))
        circle(x, by - s, 11, (38, 90, 52))
    tx = bx + flip * int(22 * math.sin(1.2))
    ty = by - 130
    for ang in (-160, -115, -70, -25, 15):
        a = math.radians(ang if flip > 0 else 180 - ang)
        line(tx, ty, tx + int(105 * math.cos(a)), ty + int(60 * math.sin(a)) + 26,
             (38, 90, 52), 9)

palm(96, 800, 1)
palm(936, 806, -1)

# the bus stop sign that has said SOON for thirteen years
line(150, 300, 150, 660, (60, 60, 70), 10)
rect(52, 196, 252, 306, WHITE)
rect(52, 196, 252, 210, BLACK)
rect(52, 292, 252, 306, BLACK)
rect(52, 196, 66, 306, BLACK)
rect(238, 196, 252, 306, BLACK)
draw_text(76, 222, "GTA 6", 6, BLACK)
draw_text(66, 272, "ARRIVING: SOON", 2, (200, 30, 40))

# bench
rect(292, 636, 772, 662, (146, 96, 52))
rect(292, 668, 772, 686, (120, 78, 42))
rect(316, 686, 336, 760, (70, 60, 66))
rect(724, 686, 744, 760, (70, 60, 66))
rect(292, 560, 772, 584, (146, 96, 52))
rect(292, 592, 772, 612, (120, 78, 42))

# the patient fan: grey hair now, cane leaning by his knee
circle(404, 512, 40, (243, 194, 144))
circle(404, 482, 34, (196, 196, 200))          # grey hair on top
rect(372, 470, 436, 492, (243, 194, 144))      # keep the face clear
circle(392, 516, 4, BLACK)
circle(420, 516, 4, BLACK)
line(392, 540, 420, 540, (150, 90, 70), 4)     # flat, patient mouth
rect(366, 552, 446, 640, (38, 150, 160))       # shirt
line(380, 580, 330, 626, (38, 150, 160), 16)   # arm resting down
rect(366, 640, 520, 676, (70, 70, 110))        # trousers, seated
rect(500, 640, 524, 716, (70, 70, 110))        # shin
rect(492, 712, 536, 730, (40, 34, 40))         # shoe
line(560, 560, 596, 716, (120, 84, 40), 7)     # the cane
circle(560, 556, 9, (120, 84, 40))

# scattered calendar pages of the wait
for (cx0, cy0, yr) in ((250, 800, "2013"), (452, 822, "2018"),
                       (700, 806, "2023"), (852, 828, "2026")):
    rect(cx0, cy0, cx0 + 92, cy0 + 56, WHITE)
    rect(cx0, cy0, cx0 + 92, cy0 + 14, (200, 30, 40))
    draw_text(cx0 + 12, cy0 + 22, yr, 3, BLACK)

# the make.fun ghost, worked into the scene on the bench
def ghost(cx, cy, r, fill, outline=None):
    """Dome body with a wavy hem; sparkle eyes drawn by the caller."""
    for y in range(cy - r, cy + r + 40):
        for x in range(cx - r, cx + r + 1):
            dx = x - cx
            if y <= cy:
                inside = dx * dx + (y - cy) * (y - cy) <= r * r
            else:
                hem = cy + r + int(9 * math.sin(dx / r * math.pi * 3))
                inside = abs(dx) <= r and y <= hem + 18
            if inside:
                px(x, y, fill)

ghost(636, 486, 84, BLACK)                     # thick black outline pass
ghost(636, 486, 74, WHITE)                     # white body inside it
sparkle(612, 470, 17, BLACK)                   # four-point sparkle eyes
sparkle(662, 470, 17, BLACK)
circle(700, 540, 15, BLACK)                    # little round hand, outlined
circle(700, 540, 11, WHITE)
circle(726, 566, 36, BLACK)                    # the magenta coin it holds
circle(726, 566, 31, MAGENTA)
star(726, 566, 17, WHITE)                      # white star on the coin

# speech bubble from the ghost
rect(566, 218, 986, 348, WHITE)
circle(566, 218, 18, WHITE)
circle(986, 218, 18, WHITE)
circle(566, 348, 18, WHITE)
circle(986, 348, 18, WHITE)
poly([(640, 348), (700, 348), (664, 402)], WHITE)
draw_text(596, 236, "I GOT PAID ON", 4, BLACK)
draw_text(596, 272, "MAKE.FUN WHILE", 4, MAGENTA)
draw_text(596, 308, "WE WAITED!", 4, BLACK)

# caption bars
rect(0, 0, W, 128, BLACK)
text_center(26, "WAITING FOR GTA 6", 9, WHITE)
text_center(88, "SINCE 2013...", 4, YELLOW)
rect(0, 876, W, H, BLACK)
text_center(898, "13 YEARS LATER: IT'S OUT!", 7, WHITE)
text_center(962, "WE'RE 31 NOW. BEST DAY EVER.", 5, YELLOW)

# ---------------------------------------------------------------- png out

def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

raw = bytearray()
for y in range(H):
    raw.append(0)
    raw += buf[y * W * 3:(y + 1) * W * 3]

png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
       + chunk(b"IEND", b""))

with open("meme.png", "wb") as f:
    f.write(png)
print("meme.png written:", len(png), "bytes")
