from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

from PIL import Image


@dataclass(frozen=True)
class FontLayout:
    glyph_width: int = 16
    glyph_height: int = 16
    glyph_count: int = 256
    columns: int = 16  # glyphs per row in PNG grid


def _bytes_per_glyph(w: int, h: int) -> int:
    return (w * h + 7) // 8


def unpack_glyphs_1bpp(data: bytes, layout: FontLayout) -> List[List[List[int]]]:
    """
    Unpack sequential 1bpp glyph stream into glyph[row][x] = 0/1

    Assumptions:
    - Row-major pixel order (left->right, top->bottom)
    - MSB-first inside each byte (bit 7 is first pixel)
    """
    w, h = layout.glyph_width, layout.glyph_height
    bpg = _bytes_per_glyph(w, h)

    glyphs: List[List[List[int]]] = []
    offset = 0

    for _ in range(layout.glyph_count):
        chunk = data[offset : offset + bpg]
        offset += bpg

        glyph: List[List[int]] = []
        bit_index = 0

        for _y in range(h):
            row: List[int] = []
            for _x in range(w):
                byte_index = bit_index // 8
                bit_in_byte = 7 - (bit_index % 8)  # MSB-first
                bit_index += 1

                if byte_index >= len(chunk):
                    row.append(0)
                else:
                    row.append((chunk[byte_index] >> bit_in_byte) & 1)
            glyph.append(row)

        glyphs.append(glyph)

    return glyphs


def pack_glyphs_1bpp(glyphs: Sequence[Sequence[Sequence[int]]], layout: FontLayout) -> bytes:
    """
    Pack glyph[row][x] = 0/1 into sequential 1bpp glyph stream.
    Same packing as unpack_glyphs_1bpp (MSB-first, row-major).
    """
    w, h = layout.glyph_width, layout.glyph_height
    bpg = _bytes_per_glyph(w, h)

    out = bytearray()

    for gi in range(layout.glyph_count):
        glyph = glyphs[gi]
        buf = bytearray(bpg)

        bit_index = 0
        for y in range(h):
            for x in range(w):
                v = 1 if glyph[y][x] else 0
                byte_index = bit_index // 8
                bit_in_byte = 7 - (bit_index % 8)
                bit_index += 1
                if v:
                    buf[byte_index] |= (1 << bit_in_byte)

        out.extend(buf)

    return bytes(out)


def glyph_to_ascii(glyph: List[List[int]], on: str = "#", off: str = ".") -> str:
    return "\n".join("".join(on if px else off for px in row) for row in glyph)


def dump_first_16_as_text(bin_path: Path, layout: FontLayout) -> None:
    data = bin_path.read_bytes()
    # force first 16 glyphs regardless of layout.glyph_count
    local_layout = FontLayout(
        glyph_width=layout.glyph_width,
        glyph_height=layout.glyph_height,
        glyph_count=16,
        columns=layout.columns,
    )
    glyphs = unpack_glyphs_1bpp(data, local_layout)

    for i, g in enumerate(glyphs):
        print(f"Glyph {i}")
        print(glyph_to_ascii(g))
        print()


def bin_to_png(bin_path: Path, png_path: Path, layout: FontLayout) -> None:
    data = bin_path.read_bytes()
    glyphs = unpack_glyphs_1bpp(data, layout)

    cols = max(1, layout.columns)
    rows = (layout.glyph_count + cols - 1) // cols

    img_w = cols * layout.glyph_width
    img_h = rows * layout.glyph_height

    img = Image.new("L", (img_w, img_h), 0)  # black bg
    px = img.load()

    for i, glyph in enumerate(glyphs):
        gx = (i % cols) * layout.glyph_width
        gy = (i // cols) * layout.glyph_height

        for y in range(layout.glyph_height):
            for x in range(layout.glyph_width):
                px[gx + x, gy + y] = 255 if glyph[y][x] else 0  # white text

    png_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(png_path)


def png_to_bin(png_path: Path, bin_path: Path, layout: FontLayout, threshold: int = 128) -> None:
    img = Image.open(png_path).convert("L")

    cols = max(1, layout.columns)
    rows = (layout.glyph_count + cols - 1) // cols
    expected_w = cols * layout.glyph_width
    expected_h = rows * layout.glyph_height

    if img.size[0] < expected_w or img.size[1] < expected_h:
        raise ValueError(
            f"PNG too small for layout: got {img.size}, need at least {(expected_w, expected_h)}"
        )

    px = img.load()

    glyphs: List[List[List[int]]] = []
    for i in range(layout.glyph_count):
        gx = (i % cols) * layout.glyph_width
        gy = (i // cols) * layout.glyph_height

        glyph: List[List[int]] = []
        for y in range(layout.glyph_height):
            row: List[int] = []
            for x in range(layout.glyph_width):
                row.append(1 if px[gx + x, gy + y] >= threshold else 0)
            glyph.append(row)

        glyphs.append(glyph)

    data = pack_glyphs_1bpp(glyphs, layout)
    bin_path.parent.mkdir(parents=True, exist_ok=True)
    bin_path.write_bytes(data)
