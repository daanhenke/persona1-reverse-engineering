"""
Archive reading and writing functionality.
"""

import struct
from pathlib import Path
from formats import SECTOR_SIZE, ARCHIVE_ENTRY_COUNTS


def read_archive(filepath, entry_count):
    """
    Read a Persona 1 scene archive.

    Returns:
        tuple: (entries, toc) where entries is a list of bytes and toc is table of contents
    """
    with open(filepath, "rb") as fh:
        data = fh.read()

    # Read table of contents (sector indices)
    toc = [struct.unpack_from("<H", data, i * 2)[0] for i in range(entry_count)]

    # Extract entries
    entries = []
    for i in range(entry_count):
        start = toc[i] * SECTOR_SIZE
        if i < entry_count - 1:
            end = toc[i + 1] * SECTOR_SIZE
            if toc[i + 1] == 0:
                end = len(data)
        else:
            end = len(data)

        if start < len(data) and end > start:
            entries.append(data[start:end])
        else:
            entries.append(b"")

    return entries, toc


def write_archive(filepath, entries):
    """
    Write entries to a Persona 1 scene archive.

    This rebuilds the entire archive with proper sector alignment.
    """
    entry_count = len(entries)

    # Calculate sector offsets for each entry
    toc_size = entry_count * 2
    toc_sectors = (toc_size + SECTOR_SIZE - 1) // SECTOR_SIZE

    # Build table of contents
    toc = []
    current_sector = toc_sectors

    for entry in entries:
        toc.append(current_sector)
        if entry:
            entry_sectors = (len(entry) + SECTOR_SIZE - 1) // SECTOR_SIZE
            current_sector += entry_sectors
        else:
            # Empty entry still takes up the TOC slot
            pass

    # Build archive data
    archive_data = bytearray()

    # Write TOC
    for sector_idx in toc:
        archive_data.extend(struct.pack("<H", sector_idx))

    # Pad to first entry
    while len(archive_data) < toc_sectors * SECTOR_SIZE:
        archive_data.append(0)

    # Write entries
    for entry in entries:
        if entry:
            archive_data.extend(entry)
            # Pad to sector boundary
            while len(archive_data) % SECTOR_SIZE != 0:
                archive_data.append(0)

    # Write to file
    with open(filepath, "wb") as fh:
        fh.write(archive_data)


def get_archive_path(archive, version, base_dir=None):
    """Get path to archive file."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent.parent

    version_paths = {
        "us": "data/dumps/us",
        "jp": "data/dumps/jp",
    }

    ver_path = version_paths.get(version.lower())
    if ver_path is None:
        raise ValueError(f"Unknown version '{version}'")

    return base_dir / ver_path / "ADV" / f"{archive.upper()}.BIN"