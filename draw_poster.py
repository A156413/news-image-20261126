#!/usr/bin/env python3
"""Paint the 26 November 2026 world-news front page (news-image-20261126).

LOCAL BUILD STEP ONLY. Run this where Pillow and the DejaVu fonts
exist; it produces entry.png, which is committed to the repository.
The submitted entrypoint (main.py) is a pure-stdlib copy of that
committed poster into $MAKEFUN_OUTPUT_DIR, because the grader's
pinned Python image has neither Pillow nor DejaVu fonts — drawing
at runtime crashed the first 20261125 attempt (exit 1).

Front page, Thursday 26 November 2026 (all stories first reported
on 26 Nov, cross-checked across several outlets):
- Lead: Pyongyang orders Switzerland to shut its diplomatic office
  and expels a senior Swiss diplomat within 48 hours, after a
  sanctions row (AFP via Manila Times).
- Pakistan's first astronaut, Muhammad Zeeshan Ali, rides China's
  Shenzhou-24 to the Tiangong station — the first foreign astronaut
  aboard China's station.
- Colombian police storm a supermarket and free 20 hostages held
  for 17 hours.
- Australia and Solomon Islands sign a landmark security pact.
- Bangladesh garment workers win a 36% wage rise.
- Briefs: 5.6-magnitude quake in Nepal's Koshi Province; Russia's
  own figures put its war dead near 500,000 (BBC); US consumer
  confidence at a near two-year high; Bellingham's wondergoal as
  Real Madrid thump PSV; Gukesh v Sindarov at the World Chess
  Championship in Geneva.
"""

import os
import struct

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BG = (248, 245, 238)
INK = (22, 22, 28)
MUTED = (74, 74, 82)
NAVY = (16, 30, 58)
CRIMSON = (172, 30, 30)
GOLD = (198, 158, 38)
TEAL = (18, 90, 96)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_lines(canvas, text, fnt, width):
    """Greedy word wrap for one paragraph."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def centred(canvas, cx, y, text, fnt, fill):
    canvas.text((cx - canvas.textlength(text, font=fnt) / 2, y),
                text, font=fnt, fill=fill)


def horizon(canvas, box, top, bottom):
    """Vertical gradient fill inside box (x, y, w, h)."""
    x, y, w, h = box
    for i in range(h):
        t = i / max(h - 1, 1)
        canvas.line([(x, y + i), (x + w, y + i)],
                    fill=tuple(int(top[c] + (bottom[c] - top[c]) * t)
                               for c in range(3)))


def paint_lead(canvas, img):
    """Lead panel: Pyongyang at night, office lights going dark."""
    x, y, w, h = 28, 118, 968, 316
    panel = Image.new("RGB", (w, h))
    p = ImageDraw.Draw(panel, "RGBA")
    horizon(p, (0, 0, w, h), (24, 28, 66), (96, 44, 52))
    # moon
    p.ellipse([w - 170, 26, w - 96, 100], fill=(238, 226, 190))
    p.ellipse([w - 158, 38, w - 108, 88], fill=(214, 200, 160))
    # skyline: towers with a few lit windows, one going dark
    import random
    rng = random.Random(26)
    bx = 18
    while bx < w - 60:
        tw = rng.randint(46, 84)
        th = rng.randint(90, 210)
        p.rectangle([bx, h - 84 - th, bx + tw, h - 84], fill=(14, 16, 34))
        for wy in range(h - 84 - th + 12, h - 92, 22):
            for wx in range(bx + 8, bx + tw - 8, 18):
                if rng.random() < 0.45:
                    p.rectangle([wx, wy, wx + 7, wy + 9],
                                fill=(255, 196, 90))
        bx += tw + 12
    # the Swiss office: white cross sign, door shutting
    p.rectangle([w - 330, h - 190, w - 150, h - 84], fill=(226, 222, 212))
    p.rectangle([w - 318, h - 178, w - 162, h - 96], outline=(22, 22, 28), width=3)
    # Swiss flag: red square, centred white cross
    fx, fy = w - 240, h - 137
    p.rectangle([fx - 28, fy - 28, fx + 28, fy + 28], fill=CRIMSON)
    p.rectangle([fx - 8, fy - 22, fx + 8, fy + 22], fill=(255, 255, 255))
    p.rectangle([fx - 22, fy - 8, fx + 22, fy + 8], fill=(255, 255, 255))
    img.paste(panel, (x, y))
    canvas = ImageDraw.Draw(img, "RGBA")
    # headline band across the bottom of the panel
    canvas.rectangle([x, y + h - 92, x + w, y + h], fill=(10, 10, 14))
    canvas.rectangle([x, y + h - 92, x + w, y + h - 88], fill=CRIMSON)
    centred(canvas, SIZE // 2, y + h - 82,
            "PYONGYANG EXPELS SWITZERLAND'S DIPLOMAT",
            load(BOLD, 33), (255, 255, 255))
    centred(canvas, SIZE // 2, y + h - 40,
            "Office ordered shut within 48 hours after a sanctions row",
            load(REG, 19), (214, 214, 214))
    canvas.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    return canvas


def paint_card(canvas, x, y, w, h, story):
    """One of four story cards: small illustration, tag, headline, deck."""
    px, py, ph = x, y, 108
    kind = story["art"]
    if kind == "rocket":
        horizon(canvas, (px, py, w, ph), (12, 24, 58), (58, 90, 140))
        canvas.ellipse([px + w - 64, py + 14, px + w - 22, py + 56],
                       fill=(240, 226, 180))
        # rocket climbing, flame below
        rx = px + w // 2 - 16
        canvas.polygon([(rx + 16, py + 14), (rx + 32, py + 52),
                        (rx + 16, py + 96), (rx, py + 52)], fill=(238, 238, 240))
        canvas.polygon([(rx, py + 52), (rx - 12, py + 76), (rx, py + 66)],
                       fill=CRIMSON)
        canvas.polygon([(rx + 32, py + 52), (rx + 44, py + 76), (rx + 32, py + 66)],
                       fill=CRIMSON)
        canvas.polygon([(rx + 16, py + 96), (rx + 6, py + 104),
                        (rx + 16, py + 98), (rx + 26, py + 104)],
                       fill=(255, 170, 40))
        canvas.ellipse([rx + 8, py + 34, rx + 24, py + 50], fill=(90, 160, 220))
        for sx in range(px + 14, px + w - 14, 34):
            canvas.ellipse([sx, py + 96, sx + 4, py + 100], fill=(255, 255, 255))
    elif kind == "rescue":
        horizon(canvas, (px, py, w, ph), (52, 66, 96), (150, 160, 178))
        # supermarket front at night, doors thrown open, light spilling out
        canvas.rectangle([px + 40, py + 30, px + w - 40, py + ph], fill=(70, 74, 88))
        canvas.rectangle([px + 40, py + 30, px + w - 40, py + 46], fill=CRIMSON)
        canvas.rectangle([px + w // 2 - 52, py + 58, px + w // 2 + 52, py + ph],
                         fill=(255, 214, 120))
        canvas.rectangle([px + w // 2 - 52, py + 58, px + w // 2 + 52, py + ph],
                         outline=INK, width=2)
        canvas.line([(px + w // 2, py + 58), (px + w // 2, py + ph)],
                    fill=INK, width=2)
        for wx in range(px + 56, px + w // 2 - 62, 30):
            canvas.rectangle([wx, py + 62, wx + 18, py + 92], fill=(190, 205, 225))
        for wx in range(px + w // 2 + 70, px + w - 56, 30):
            canvas.rectangle([wx, py + 62, wx + 18, py + 92], fill=(190, 205, 225))
        canvas.text((px + w // 2 - 40, py + 8), "17 HOURS", font=load(BOLD, 16),
                    fill=(255, 255, 255))
    elif kind == "pact":
        horizon(canvas, (px, py, w, ph), (14, 70, 70), (90, 150, 150))
        # two flags on poles, clasped hands below
        for fx, col in ((px + 60, (0, 40, 90)), (px + w - 140, (0, 90, 60))):
            canvas.rectangle([fx, py + 18, fx + 6, py + 96], fill=(220, 210, 190))
            canvas.rectangle([fx + 6, py + 22, fx + 74, py + 58], fill=col)
            canvas.ellipse([fx + 22, py + 30, fx + 58, py + 50], fill=GOLD)
        canvas.ellipse([px + w // 2 - 52, py + 74, px + w // 2 + 52, py + 104],
                       fill=(238, 214, 170))
        canvas.arc([px + w // 2 - 52, py + 74, px + w // 2 + 52, py + 104],
                   200, 340, fill=INK, width=3)
        canvas.line([(px + w // 2 - 30, py + 90), (px + w // 2 + 30, py + 90)],
                    fill=INK, width=3)
    else:  # factory / wages
        horizon(canvas, (px, py, w, ph), (120, 60, 30), (210, 140, 70))
        canvas.rectangle([px + 30, py + 62, px + w - 30, py + ph], fill=(96, 52, 24))
        canvas.rectangle([px + 30, py + 62, px + w - 30, py + 78], fill=(140, 80, 36))
        for wx in range(px + 46, px + w - 46, 34):
            canvas.rectangle([wx, py + 88, wx + 20, py + 112], fill=(255, 214, 120))
        # rising arrow over the roofline
        canvas.line([(px + 60, py + 52), (px + w - 70, py + 16)], fill=CRIMSON, width=6)
        canvas.polygon([(px + w - 70, py + 16), (px + w - 96, py + 18),
                        (px + w - 74, py + 38)], fill=CRIMSON)
        canvas.text((px + w - 118, py + 34), "+36%", font=load(BOLD, 26),
                    fill=CRIMSON)
    canvas.rectangle([px, py, px + w, py + ph], outline=INK, width=2)
    ty = y + ph + 8
    canvas.text((x, ty), story["tag"], font=load(BOLD, 14), fill=CRIMSON)
    hy = ty + 20
    for line in story["head"].split("\n"):
        canvas.text((x, hy), line, font=load(BOLD, 22), fill=INK)
        hy += 25
    dy = hy + 2
    for line in fit_lines(canvas, story["deck"], load(REG, 15), w):
        canvas.text((x, dy), line, font=load(REG, 15), fill=MUTED)
        dy += 18


def paint_page():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    canvas = ImageDraw.Draw(img, "RGBA")
    # masthead
    canvas.rectangle([0, 0, SIZE, 100], fill=NAVY)
    canvas.rectangle([0, 100, SIZE, 104], fill=GOLD)
    centred(canvas, SIZE // 2, 10, "THE WORLD TODAY", load(SERIF, 52), BG)
    centred(canvas, SIZE // 2, 70,
            "THURSDAY  •  26 NOVEMBER 2026  •  ONE DAY, ONE PICTURE",
            load(BOLD, 19), GOLD)
    canvas = paint_lead(canvas, img)
    stories = [
        {"tag": "SPACE  •  CHINA'S STATION",
         "head": "PAKISTAN'S FIRST\nASTRONAUT IN ORBIT",
         "deck": "Muhammad Zeeshan Ali rides Shenzhou-24 to Tiangong — the first "
                 "foreign astronaut aboard China's space station.",
         "art": "rocket"},
        {"tag": "COLOMBIA  •  RESCUE",
         "head": "20 HOSTAGES FREED\nAFTER 17-HOUR SIEGE",
         "deck": "Police storm a supermarket and free every hostage held "
                 "overnight; the gunman is in custody.",
         "art": "rescue"},
        {"tag": "PACIFIC  •  SECURITY",
         "head": "AUSTRALIA SIGNS\nISLANDS SECURITY PACT",
         "deck": "Canberra and Solomon Islands ink a landmark deal that "
                 "reshapes security across the South Pacific.",
         "art": "pact"},
        {"tag": "BANGLADESH  •  WORKERS",
         "head": "GARMENT WORKERS\nWIN 36% PAY RISE",
         "deck": "Months of strikes end in a big wage deal for the workers "
                 "who stitch the world's clothes.",
         "art": "factory"},
    ]
    cw, gap = 472, 24
    positions = [(28, 448), (524, 448), (28, 682), (524, 682)]
    for story, (cx, cy) in zip(stories, positions):
        paint_card(canvas, cx, cy, cw, 226, story)
    # also-today strip
    by = 918
    canvas.rectangle([28, by, 996, by + 2], fill=INK)
    canvas.text((28, by + 10), "ALSO TODAY", font=load(BOLD, 17), fill=CRIMSON)
    briefs = ("Nepal shaken by a 5.6 quake near the China border  •  "
              "Russia's own figures put its war dead near 500,000  •  "
              "US consumer confidence hits a near two-year high  •  "
              "Bellingham's wondergoal as Real Madrid thump PSV")
    yy = by + 36
    for line in fit_lines(canvas, briefs, load(REG, 16), 940):
        canvas.text((28, yy), line, font=load(REG, 16), fill=INK)
        yy += 21
    canvas.rectangle([0, 1000, SIZE, SIZE], fill=NAVY)
    centred(canvas, SIZE // 2, 1006, "26 NOVEMBER 2026  —  THE DAY IN ONE IMAGE",
            load(BOLD, 16), BG)
    return img


def self_check(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise RuntimeError(f"{path} is not a PNG with an IHDR")
    w, h = struct.unpack(">II", head[16:24])
    if (w, h) != (SIZE, SIZE):
        raise RuntimeError(f"poster is {w}x{h}, not {SIZE} square")
    img = Image.open(path)
    palette = img.convert("RGB").getcolors(maxcolors=1 << 24)
    if not palette or len(palette) < 100:
        raise RuntimeError("poster looks blank: too few distinct colours")
    size = os.path.getsize(path)
    if size < 10_000:
        raise RuntimeError(f"poster suspiciously small: {size} bytes")
    if size > 1_048_576:
        raise RuntimeError(f"poster over 1 MiB: {size} bytes")
    return size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    tmp = out + ".tmp"
    img = paint_page()
    img.save(tmp, format="PNG")
    size = self_check(tmp)
    os.replace(tmp, out)
    print("wrote", out, img.size, f"{size} bytes")


if __name__ == "__main__":
    main()
