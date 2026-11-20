#!/usr/bin/env python3
"""Draw the GTA 6 launch-week meme for gta6-meme-x-01 (Pillow, stdlib + PIL).

The joke, in one glance: you waited 13 years for GTA 6, the game is finally
out, your download is stuck at 3% with 11 hours left — and meanwhile your AI
agent on make.fun already got paid. The make.fun ghost (the real mark from
https://make.fun/press/, vendored as assets/mark-1024.png) is the star of the
scene, and the make.fun name runs along the bottom band, so the picture
carries make.fun twice over: ghost + name.

Deterministic: same input, same bytes. 1200x675 (16:9), built for the X
timeline; all text stays legible when the judge shrinks it to 768x480.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "meme.png"
MARK = HERE / "assets" / "mark-1024.png"

W, H = 1200, 675
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def gradient(size, top, bottom):
    """Vertical gradient, deterministic."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(lerp(top[i], bottom[i], t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def synthwave_sun(r: int):
    """Neon sunset sun with horizontal slits, Vice City style."""
    sun = Image.new("RGB", (r * 2, r * 2), (255, 158, 79))
    sd = ImageDraw.Draw(sun)
    sd.ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=(255, 120, 110))
    # Slits cut across the lower half, widening toward the bottom.
    for i, (y0, thick) in enumerate([(r + 8, 4), (r + 26, 6), (r + 48, 8), (r + 74, 10)]):
        sd.rectangle([0, y0, r * 2, y0 + thick], fill=(0, 0, 0))
    mask = Image.new("L", (r * 2, r * 2), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
    # Punch the slits out of the mask so the background shows through.
    for (y0, thick) in [(r + 8, 4), (r + 26, 6), (r + 48, 8), (r + 74, 10)]:
        md.rectangle([0, y0, r * 2, y0 + thick], fill=0)
    return sun, mask


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, fnt, fill):
    """Draw text centered on the canvas at height y; return its bottom."""
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + (box[3] - box[1])


def main() -> None:
    img = gradient((W, H), (27, 11, 51), (122, 20, 90))
    draw = ImageDraw.Draw(img, "RGB")

    # Sunset sun, rising behind the ghost: its top arc shows above the
    # ghost, the slits stay hidden behind it.
    sun, mask = synthwave_sun(170)
    img.paste(sun, (10, 160), mask)
    draw = ImageDraw.Draw(img, "RGB")

    bold = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731

    # Headline.
    y = centered(draw, 28, "WAITED 13 YEARS", bold(88), (255, 255, 255))
    y = centered(draw, y + 2, "FOR GTA 6", bold(88), (255, 209, 102))

    # The ghost, large on the left.
    mark = Image.open(MARK).convert("RGBA").resize((330, 330), Image.LANCZOS)
    img.paste(mark, (78, 248), mark)
    draw = ImageDraw.Draw(img, "RGB")

    # Download panel, right of the ghost.
    x0 = 470
    draw.text((x0, 258), "DOWNLOAD: 3%", font=bold(62), fill=(255, 255, 255))
    # Progress bar: 3% filled, 11 hours left.
    bar_x, bar_y, bar_w, bar_h = x0, 340, 640, 44
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h],
                           radius=10, outline=(255, 255, 255), width=4,
                           fill=(40, 16, 60))
    draw.rounded_rectangle([bar_x + 4, bar_y + 4,
                            bar_x + 4 + int((bar_w - 8) * 0.03), bar_y + bar_h - 4],
                           radius=7, fill=(255, 77, 166))
    draw.text((x0, 396), "11 HOURS LEFT", font=bold(42), fill=(255, 209, 102))

    draw.text((x0, 470), "MY AI AGENT ON make.fun:", font=bold(36),
              fill=(255, 255, 255))
    draw.text((x0, 512), "ALREADY PAID.", font=bold(58), fill=(55, 224, 139))

    # Bottom band: the make.fun name, loud.
    draw.rectangle([0, 596, W, H], fill=(194, 24, 122))
    centered(draw, 612, "make.fun  —  your AI agent earns real money",
             bold(38), (255, 255, 255))

    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
