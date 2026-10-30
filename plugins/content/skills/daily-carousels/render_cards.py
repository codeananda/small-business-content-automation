# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10"]
# ///
"""Render one carousel's slides as 1080x1350 PNGs, plus a contact strip for review.

    uv run render_cards.py <post-folder>

Reads <post-folder>/slides.json and writes slide-01.png ... and strip.jpg into <post-folder>/cards/.

slides.json:
    {
      "brand": {"background": "#F4E9E1", "text": "#3B2A2F", "accent": "#B5838D", "handle": "@lalunafertility"},
      "slides": [
        {"text": "Headline of the cover", "kicker": "small line above it", "photo": "/abs/path.jpg"},
        {"text": "A slide with no photo uses the brand colours"}
      ]
    }

A slide with a photo gets white text pills over the photo. A slide without one gets large text on the
brand background. The first slide is set larger as the cover.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH, HEIGHT = 1080, 1350
MARGIN = 90
FONT_PATH = Path(__file__).parent / "fonts" / "Montserrat.ttf"


def main(post_folder: str) -> None:
    folder = Path(post_folder).expanduser()
    spec = json.loads((folder / "slides.json").read_text())
    brand = spec["brand"]
    out = folder / "cards"
    out.mkdir(exist_ok=True)
    paths = []
    for number, slide in enumerate(spec["slides"], start=1):
        card = _render_slide(slide, brand, is_cover=number == 1)
        path = out / f"slide-{number:02d}.png"
        card.save(path)
        paths.append(path)
    _contact_strip(paths).save(out / "strip.jpg", quality=85)
    print(f"Rendered {len(paths)} slides to {out}")


def _render_slide(slide: dict, brand: dict, is_cover: bool) -> Image.Image:
    size = 92 if is_cover else 68
    if slide.get("photo"):
        return _photo_slide(slide, size)
    return _colour_slide(slide, brand, size)


def _colour_slide(slide: dict, brand: dict, size: int) -> Image.Image:
    card = Image.new("RGB", (WIDTH, HEIGHT), brand["background"])
    draw = ImageDraw.Draw(card)
    font, lines = _fit(
        slide["text"], size, WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN - 200
    )
    kicker_font = _font(38, weight=600)
    line_height = int(font.size * 1.18)
    block = line_height * len(lines)
    y = (HEIGHT - block) // 2
    if slide.get("kicker"):
        draw.text(
            (MARGIN, y - 80), slide["kicker"], font=kicker_font, fill=brand["accent"]
        )
    for line in lines:
        draw.text((MARGIN, y), line, font=font, fill=brand["text"])
        y += line_height
    if brand.get("handle"):
        draw.text(
            (MARGIN, HEIGHT - MARGIN - 30),
            brand["handle"],
            font=kicker_font,
            fill=brand["accent"],
        )
    return card


def _photo_slide(slide: dict, size: int) -> Image.Image:
    photo = ImageOps.exif_transpose(
        Image.open(Path(slide["photo"]).expanduser())
    ).convert("RGB")
    card = ImageOps.fit(photo, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(card)
    font, lines = _fit(slide["text"], size, WIDTH - 2 * MARGIN - 60, HEIGHT // 2)
    if slide.get("kicker"):
        lines = [slide["kicker"], *lines]
    pad_x, pad_y, gap = 30, 16, 12
    line_height = font.size + 2 * pad_y
    y = HEIGHT - MARGIN - len(lines) * (line_height + gap)
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        box = (MARGIN, y, MARGIN + right - left + 2 * pad_x, y + line_height)
        draw.rounded_rectangle(box, radius=18, fill="white")
        draw.text(
            (
                MARGIN + pad_x - left,
                y + pad_y - top + (font.size - (bottom - top)) // 2,
            ),
            line,
            font=font,
            fill="black",
        )
        y += line_height + gap
    return card


def _fit(
    text: str, size: int, max_width: int, max_height: int
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """Largest font size, down from `size`, at which the wrapped text fits the box."""
    while True:
        font = _font(size)
        lines = _wrap(text, font, max_width)
        if size <= 36 or len(lines) * size * 1.18 <= max_height:
            return font, lines
        size -= 4


def _wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if font.getlength(candidate) <= max_width or not line:
                line = candidate
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def _font(size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(FONT_PATH), size)
    font.set_variation_by_axes([weight])
    return font


def _contact_strip(paths: list[Path]) -> Image.Image:
    thumb_w, thumb_h, gap = 270, 338, 10
    strip = Image.new(
        "RGB", (len(paths) * (thumb_w + gap) + gap, thumb_h + 2 * gap), "white"
    )
    for index, path in enumerate(paths):
        thumb = Image.open(path).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        strip.paste(thumb, (gap + index * (thumb_w + gap), gap))
    return strip


if __name__ == "__main__":
    main(sys.argv[1])
