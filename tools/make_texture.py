# /// script
# dependencies = ["pillow"]
# ///
"""Draws the 16x16 belt texture and the pack icon.

Run: uv run tools/make_texture.py [path/to/meme.jpg]
Always redraws the belt texture. With a meme image path, also redraws pack.png for both packs.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Grip (where the fist holds it) is the top-right corner; the model's display
# transforms rotate the sprite so this end sits in the hand and the loop hangs down.
BELT = """
................
...........oo...
........ooobboo.
......oobbbbbobo
.....obbhooboobo
...oobhoo.oboobo
..obhbo..obboobo
..obhoo..obo.obo
.obho...obbo.obo
.obo....obo.gssg
.obo...obbo.s.bs
.ohbo.obbo..s.bs
.obboobbo...gssg
..obbbbo.....oo.
...oooo.........
................
"""

PALETTE = {
    ".": (0, 0, 0, 0),
    "o": (61, 40, 23, 255),  # leather edge
    "b": (123, 82, 51, 255),  # leather
    "h": (163, 115, 74, 255),  # leather highlight
    "s": (212, 212, 212, 255),  # buckle
    "g": (140, 140, 140, 255),  # buckle shade
}


def draw_belt() -> Image.Image:
    rows = BELT.strip().splitlines()
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), "belt grid must be 16x16"
    img = Image.new("RGBA", (16, 16))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            img.putpixel((x, y), PALETTE[ch])
    return img


def draw_icon(meme: Path) -> Image.Image:
    src = Image.open(meme).convert("RGB")
    side = min(src.size)
    top = (src.height - side) // 2
    left = (src.width - side) // 2
    return src.crop((left, top, left + side, top + side)).resize((256, 256), Image.LANCZOS)


def main() -> None:
    meme = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    out = ROOT / "resourcepack" / "assets" / "clanka_spanka" / "textures" / "item" / "clanka_spanka.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    draw_belt().save(out)
    print(f"wrote {out}")

    if meme is None:
        return
    icon = draw_icon(meme)
    for pack in ("resourcepack", "datapack"):
        path = ROOT / pack / "pack.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        icon.save(path)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
