#!/usr/bin/env python3
"""
Persona 1 (PS1) Scene Tool

A tool for decompiling and recompiling Persona 1 scene archives.
Allows editing scripts and messages, then rebuilding the archive.
"""

import argparse
import sys
from pathlib import Path

from archive import read_archive, write_archive, get_archive_path
from scene import Scene
from message import Encoding
from formats import ARCHIVE_ENTRY_COUNTS


def cmd_extract(args):
    """Extract scenes from archive to editable format."""
    archive = args.archive.upper()
    version = args.version.lower()

    # Load encoding
    if args.encoding:
        enc_path = Path(args.encoding)
    else:
        # Auto-detect from common locations
        base = Path(__file__).parent.parent.parent
        enc_path = base / f"old/encoding_{version}.txt"
        if not enc_path.exists():
            enc_path = base / f"encoding_{version}.txt"
        if not enc_path.exists():
            print(f"ERROR: Encoding file not found. Tried: {enc_path}", file=sys.stderr)
            sys.exit(1)

    print(f"  Using encoding: {enc_path}")
    enc = Encoding.load(enc_path)

    # Get archive path
    try:
        archive_path = get_archive_path(archive, version)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if not archive_path.exists():
        print(f"ERROR: Archive not found: {archive_path}", file=sys.stderr)
        sys.exit(1)

    # Get entry count
    count = ARCHIVE_ENTRY_COUNTS.get(archive)
    if count is None:
        print(f"ERROR: Unknown archive '{archive}'", file=sys.stderr)
        sys.exit(1)

    # Read archive
    print(f"Reading archive: {archive_path}")
    entries, toc = read_archive(archive_path, count)

    # Extract entries
    output_dir = Path(args.output) if args.output else Path(f"scenes/{archive.lower()}_{version}")
    output_dir.mkdir(parents=True, exist_ok=True)

    extracted = 0
    for i in range(count):
        if args.entry is not None and i != args.entry:
            continue

        raw = entries[i]
        if not raw or len(raw) < 0x10C8:
            continue

        scene = Scene.parse(raw)
        if scene is None:
            continue

        entry_dir = output_dir / f"{i:03d}"
        scene.extract(entry_dir, enc)

        ns = len(scene.scripts)
        nm = len(scene.messages)
        print(f"  [{i:03d}] {len(raw):6d} bytes  scripts={ns}  msgs={nm}")
        extracted += 1

    print(f"\nExtracted {extracted} entries to {output_dir}/")


def cmd_build(args):
    """Build archive from extracted scenes."""
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    archive = args.archive.upper()
    version = args.version.lower()

    # Load encoding
    if args.encoding:
        enc_path = Path(args.encoding)
    else:
        # Auto-detect from common locations
        base = Path(__file__).parent.parent.parent
        enc_path = base / f"old/encoding_{version}.txt"
        if not enc_path.exists():
            enc_path = base / f"encoding_{version}.txt"
        if not enc_path.exists():
            print(f"ERROR: Encoding file not found. Tried: {enc_path}", file=sys.stderr)
            sys.exit(1)

    print(f"  Using encoding: {enc_path}")
    enc = Encoding.load(enc_path)

    # Get entry count
    count = ARCHIVE_ENTRY_COUNTS.get(archive)
    if count is None:
        print(f"ERROR: Unknown archive '{archive}'", file=sys.stderr)
        sys.exit(1)

    # Build entries
    print(f"Building archive entries...")
    entries = []
    built = 0

    for i in range(count):
        if args.entry is not None and i != args.entry:
            # If specific entry requested, load empty for others
            entries.append(b"")
            continue

        entry_dir = input_dir / f"{i:03d}"
        if entry_dir.exists() and (entry_dir / "metadata.json").exists():
            scene = Scene.load(entry_dir, enc)
            raw = scene.build()
            entries.append(raw)
            print(f"  [{i:03d}] {len(raw):6d} bytes")
            built += 1
        else:
            entries.append(b"")

    # Write archive
    output_path = Path(args.output) if args.output else Path(f"{archive}_{version}_rebuilt.BIN")
    print(f"\nWriting archive: {output_path}")
    write_archive(output_path, entries)

    print(f"Built {built} entries")


def cmd_roundtrip(args):
    """Test round-trip (extract then rebuild and compare)."""
    archive = args.archive.upper()
    version = args.version.lower()
    entry_id = args.entry

    # Load encoding
    if args.encoding:
        enc_path = Path(args.encoding)
    else:
        # Auto-detect from common locations
        base = Path(__file__).parent.parent.parent
        enc_path = base / f"old/encoding_{version}.txt"
        if not enc_path.exists():
            enc_path = base / f"encoding_{version}.txt"
        if not enc_path.exists():
            print(f"ERROR: Encoding file not found. Tried: {enc_path}", file=sys.stderr)
            sys.exit(1)

    print(f"  Using encoding: {enc_path}")
    enc = Encoding.load(enc_path)

    # Get archive
    archive_path = get_archive_path(archive, version)
    count = ARCHIVE_ENTRY_COUNTS.get(archive)

    # Read original
    entries, toc = read_archive(archive_path, count)
    original = entries[entry_id]

    if not original:
        print(f"ERROR: Entry {entry_id} is empty", file=sys.stderr)
        sys.exit(1)

    print(f"Original size: {len(original)} bytes")

    # Parse
    scene = Scene.parse(original)
    if scene is None:
        print(f"ERROR: Failed to parse entry {entry_id}", file=sys.stderr)
        sys.exit(1)

    print(f"  Scripts: {len(scene.scripts)}")
    print(f"  Messages: {len(scene.messages)}")

    # Extract to temp
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir) / f"{entry_id:03d}"
        scene.extract(tmppath, enc)
        print(f"  Extracted to temp")

        # Reload
        scene2 = Scene.load(tmppath, enc)
        print(f"  Reloaded from temp")

        # Rebuild
        rebuilt = scene2.build()
        print(f"Rebuilt size:  {len(rebuilt)} bytes")

        # Compare
        if original == rebuilt:
            print("\nSUCCESS: Round-trip produced identical binary!")
        else:
            print(f"\nFAILED: Binaries differ")
            print(f"  Original: {len(original)} bytes")
            print(f"  Rebuilt:  {len(rebuilt)} bytes")

            # Find first difference
            min_len = min(len(original), len(rebuilt))
            for i in range(min_len):
                if original[i] != rebuilt[i]:
                    print(f"  First difference at offset 0x{i:04X}")
                    print(f"    Original: {original[i]:02X}")
                    print(f"    Rebuilt:  {rebuilt[i]:02X}")
                    break


def main():
    parser = argparse.ArgumentParser(
        description="Persona 1 Scene Tool - Extract, edit, and rebuild scene archives"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract scenes to editable format")
    extract_parser.add_argument("archive", help="Archive name (E0, E1, E2, E3)")
    extract_parser.add_argument("version", help="Version (us or jp)")
    extract_parser.add_argument("-o", "--output", help="Output directory")
    extract_parser.add_argument("-e", "--entry", type=int, help="Extract single entry")
    extract_parser.add_argument("--encoding", help="Encoding table file")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build archive from extracted scenes")
    build_parser.add_argument("archive", help="Archive name (E0, E1, E2, E3)")
    build_parser.add_argument("version", help="Version (us or jp)")
    build_parser.add_argument("input", help="Input directory with extracted scenes")
    build_parser.add_argument("-o", "--output", help="Output archive file")
    build_parser.add_argument("-e", "--entry", type=int, help="Build single entry")
    build_parser.add_argument("--encoding", help="Encoding table file")

    # Round-trip test command
    roundtrip_parser = subparsers.add_parser("test", help="Test round-trip for an entry")
    roundtrip_parser.add_argument("archive", help="Archive name (E0, E1, E2, E3)")
    roundtrip_parser.add_argument("version", help="Version (us or jp)")
    roundtrip_parser.add_argument("entry", type=int, help="Entry to test")
    roundtrip_parser.add_argument("--encoding", help="Encoding table file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "test":
        cmd_roundtrip(args)


if __name__ == "__main__":
    main()