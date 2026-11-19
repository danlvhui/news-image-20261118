#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic.

Runs locally only (the entrypoint main.py just copies the PNG this script
produces). Everything is drawn with PIL primitives and text: no photos, no
copied artwork, no AI-generated imagery.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 244, 233)      # newsprint cream
INK = (26, 26, 26)        # near-black
RED = (178, 34, 30)       # masthead red
BLUE = (31, 73, 125)      # icon blue
GOLD = (176, 124, 22)     # icon gold
GREY = (90, 88, 80)       # secondary text

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

STORIES = [
    ("summit", "TRUMP LANDS IN SHENZHEN",
     "Xi and Putin meet a day before the first-ever US\u2013China\u2013Russia trilateral."),
    ("drone", "IRAN DRONES HIT US BASE IN KUWAIT",
     "Tehran says its drones struck US platforms at Ali Al Salem; Gulf defences intercept."),
    ("gaza", "ISRAEL MOVES INTO CENTRAL GAZA",
     "First major ground operation since the October 2025 ceasefire, the army says."),
    ("trade", "INDIA\u2013US TRADE DEAL NEARLY DONE",
     "Signing delayed until Washington finalises a new tariff framework."),
    ("storm", "CYCLONE AKVAN STRENGTHENS",
     "Severe storm over the Bay of Bengal; India\u2019s east coast braces for landfall."),
    ("sanction", "AUSTRALIA SANCTIONS SETTLER LEADER",
     "Daniella Weiss and settler entities sanctioned over West Bank expansion."),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon(draw, kind, x, y, s, color):
    """Simple geometric pictogram, s = box size."""
    if kind == "summit":
        # three leaders: three circles above a table line
        r = s * 0.16
        for i, cx in enumerate((x + s * 0.22, x + s * 0.5, x + s * 0.78)):
            draw.ellipse([cx - r, y + s * 0.18, cx + r, y + s * 0.18 + 2 * r],
                         fill=color)
            draw.rectangle([cx - r * 1.15, y + s * 0.55, cx + r * 1.15, y + s * 0.82],
                           fill=color)
        draw.line([x + s * 0.08, y + s * 0.88, x + s * 0.92, y + s * 0.88],
                  fill=color, width=4)
    elif kind == "drone":
        # quadcopter: body + 4 rotors, dashed flight path
        cx, cy = x + s * 0.5, y + s * 0.45
        draw.ellipse([cx - s * 0.14, cy - s * 0.1, cx + s * 0.14, cy + s * 0.1],
                     fill=color)
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            rx, ry = cx + dx * s * 0.3, cy + dy * s * 0.22
            draw.line([cx, cy, rx, ry], fill=color, width=4)
            draw.ellipse([rx - s * 0.11, ry - 3, rx + s * 0.11, ry + 3], fill=color)
        for i in range(5):
            px = x + s * 0.08 + i * s * 0.18
            draw.ellipse([px, y + s * 0.82, px + 7, y + s * 0.82 + 7], fill=color)
    elif kind == "gaza":
        # tank silhouette: hull, turret, barrel, tracks
        draw.rectangle([x + s * 0.14, y + s * 0.42, x + s * 0.8, y + s * 0.62],
                       fill=color)
        draw.rectangle([x + s * 0.38, y + s * 0.26, x + s * 0.62, y + s * 0.44],
                       fill=color)
        draw.line([x + s * 0.62, y + s * 0.32, x + s * 0.9, y + s * 0.28],
                  fill=color, width=6)
        draw.rectangle([x + s * 0.1, y + s * 0.64, x + s * 0.84, y + s * 0.8],
                       fill=color)
        for wx in (0.22, 0.42, 0.62):
            draw.ellipse([x + s * wx - 6, y + s * 0.67, x + s * wx + 6, y + s * 0.67 + 12],
                         fill=BG)
    elif kind == "trade":
        # two shaking hands, simplified: two opposing arrows + dollar coin
        draw.ellipse([x + s * 0.32, y + s * 0.22, x + s * 0.68, y + s * 0.58],
                     outline=color, width=6)
        draw.text((x + s * 0.5, y + s * 0.4), "$", font=SANS_B(int(s * 0.3)),
                  fill=color, anchor="mm")
        draw.line([x + s * 0.08, y + s * 0.76, x + s * 0.4, y + s * 0.76],
                  fill=color, width=5)
        draw.polygon([(x + s * 0.4, y + s * 0.68), (x + s * 0.4, y + s * 0.84),
                      (x + s * 0.52, y + s * 0.76)], fill=color)
        draw.line([x + s * 0.92, y + s * 0.76, x + s * 0.6, y + s * 0.76],
                  fill=color, width=5)
        draw.polygon([(x + s * 0.6, y + s * 0.68), (x + s * 0.6, y + s * 0.84),
                      (x + s * 0.48, y + s * 0.76)], fill=color)
    elif kind == "storm":
        # cyclone spiral: concentric arcs + rain drops
        cx, cy = x + s * 0.5, y + s * 0.42
        for i, r in enumerate((s * 0.34, s * 0.25, s * 0.16)):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=200 * i, end=200 * i + 240,
                     fill=color, width=5)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
        for dx in (-0.3, 0.0, 0.3):
            rx = x + s * (0.5 + dx)
            draw.line([rx, y + s * 0.78, rx - 5, y + s * 0.9], fill=color, width=4)
    elif kind == "sanction":
        # prohibition sign over a small building
        cx, cy = x + s * 0.5, y + s * 0.45
        draw.rectangle([x + s * 0.3, cy - s * 0.08, x + s * 0.7, cy + s * 0.2],
                       fill=color)
        draw.polygon([(x + s * 0.24, cy - s * 0.08), (x + s * 0.5, cy - s * 0.26),
                      (x + s * 0.76, cy - s * 0.08)], fill=color)
        draw.rectangle([x + s * 0.34, cy + s * 0.24, x + s * 0.66, cy + s * 0.34],
                       fill=BG)
        draw.ellipse([cx - s * 0.34, cy - s * 0.34, cx + s * 0.34, cy + s * 0.34],
                     outline=RED, width=7)
        draw.line([cx - s * 0.24, cy + s * 0.24, cx + s * 0.24, cy - s * 0.24],
                  fill=RED, width=7)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 56  # margin

    # --- masthead ---
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=SANS_B(30),
           fill=RED, anchor="mm")
    d.text((W // 2, 118), "WORLD NEWS", font=SERIF_B(96), fill=INK, anchor="mm")
    d.line([mx, 172, W - mx, 172], fill=INK, width=4)
    d.line([mx, 180, W - mx, 180], fill=INK, width=2)

    # --- date, the anchor of the whole image ---
    d.text((W // 2, 232), "Wednesday, 18 November 2026", font=SERIF_B(52),
           fill=INK, anchor="mm")
    d.text((W // 2, 282), "Six stories that defined the day \u2014 from Shenzhen to the Gulf",
           font=SANS(26), fill=GREY, anchor="mm")
    d.line([mx, 312, W - mx, 312], fill=RED, width=3)

    # --- stories ---
    y = 330
    row_h = 106
    colors = [BLUE, RED, INK, GOLD, BLUE, RED]
    for i, (kind, head, sub) in enumerate(STORIES):
        box = 84
        # icon box
        d.rectangle([mx, y, mx + box, y + box], outline=colors[i], width=3)
        icon(d, kind, mx + 4, y + 4, box - 8, colors[i])
        tx = mx + box + 22
        d.text((tx, y + 6), head, font=SANS_B(30), fill=INK)
        lines = wrap(d, sub, SANS(23), W - mx - tx - 8)
        ly = y + 48
        for ln in lines[:2]:
            d.text((tx, ly), ln, font=SANS(23), fill=GREY)
            ly += 28
        y += row_h
        if i < len(STORIES) - 1:
            d.line([mx, y - 8, W - mx, y - 8], fill=(200, 194, 178), width=1)

    # --- footer ---
    d.line([mx, 972, W - mx, 972], fill=INK, width=2)
    d.text((W // 2, 996),
           "Every event above happened or was first reported on 18 November 2026.",
           font=SANS(20), fill=GREY, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
