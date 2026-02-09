from __future__ import annotations

import argparse
from pathlib import Path

from .font.font import (
    FontLayout,
    bin_to_png,
    dump_first_16_as_text,
    png_to_bin,
)

from .event.archive import (
  unpack_event_archive,
  repack_event_archive
)


def _add_layout_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--width", type=int, default=16, help="Glyph width in pixels")
    p.add_argument("--height", type=int, default=16, help="Glyph height in pixels")
    p.add_argument("--count", type=int, default=2048, help="Number of glyphs")
    p.add_argument("--cols", type=int, default=16, help="Glyph columns in PNG grid")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="p1patch")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # p1patch font ...
    font = sub.add_parser("font", help="Font tools")
    font_sub = font.add_subparsers(dest="font_cmd", required=True)

    # p1patch font dump
    font_dump = font_sub.add_parser("dump", help="Dump a font BIN to PNG, or print as text")
    font_dump.add_argument("bin", type=Path, help="Input font binary")
    font_dump.add_argument("png", type=Path, nargs="?", help="Output PNG (omit when using --text)")
    font_dump.add_argument("--text", action="store_true", help="Print first 16 glyphs as ASCII art")
    _add_layout_args(font_dump)

    # p1patch font create
    font_create = font_sub.add_parser("create", help="Create a font BIN from a PNG grid")
    font_create.add_argument("png", type=Path, help="Input PNG grid (black bg, white text)")
    font_create.add_argument("bin", type=Path, help="Output font binary")
    font_create.add_argument("--threshold", type=int, default=128, help="White threshold (0-255)")
    _add_layout_args(font_create)

    # p1patch event ...
    event = sub.add_parser("event", help="Event tools")
    event_sub = event.add_subparsers(dest="event_cmd", required=True)

    # p1patch event extract
    event_extract = event_sub.add_parser("extract-archive", help="Extract an event archive file into a set of events")
    event_extract.add_argument("bin", type=Path, help="Input event archive")
    event_extract.add_argument("events_dir", type=Path, help="Output directory")

    # p1patch event repack
    event_extract = event_sub.add_parser("repack-archive", help="Repack an event archive file from a set of events")
    event_extract.add_argument("events_dir", type=Path, help="Input directory")
    event_extract.add_argument("bin", type=Path, help="Output event archive")

    args = parser.parse_args(argv)

    if args.cmd == "font" and args.font_cmd == "dump":
      layout = FontLayout(
        glyph_width=args.width,
        glyph_height=args.height,
        glyph_count=args.count,
        columns=args.cols,
      )

      if args.text:
        dump_first_16_as_text(args.bin, layout)
        return

      if args.png is None:
        parser.error("p1patch font dump: missing <out.png> (or use --text)")
      bin_to_png(args.bin, args.png, layout)
      return

    if args.cmd == "font" and args.font_cmd == "create":
      layout = FontLayout(
        glyph_width=args.width,
        glyph_height=args.height,
        glyph_count=args.count,
        columns=args.cols,
      )
      png_to_bin(args.png, args.bin, layout, threshold=args.threshold)
      return

    if args.cmd == "event" and args.event_cmd == "extract-archive":
      print(args.bin)
      unpack_event_archive(args.bin, args.events_dir)
      return

    if args.cmd == "event" and args.event_cmd == "repack-archive":
      print(args.bin)
      repack_event_archive(args.events_dir, args.bin)
      return

    parser.error("Unknown command")
