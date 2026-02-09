from pathlib import Path
from struct import pack, unpack_from

from ..common.constants import SECTOR_SIZE


def pad_to_sector(out: bytearray, pad_byte: int = 0) -> None:
    missing = (-len(out)) % SECTOR_SIZE
    if missing:
        out.extend(bytes([pad_byte]) * missing)

def glob_files_sorted(
    entries_dir: str | Path,
    pattern: str = "*",
    recursive: bool = False,
) -> list[Path]:
    base = Path(entries_dir)
    it = base.rglob(pattern) if recursive else base.glob(pattern)
    return sorted((p for p in it if p.is_file()), key=lambda p: p.name)

def unpack_event_archive(archive_path: Path, output_path: Path):
  data = archive_path.read_bytes()

  toc = []
  for i in range (0x100):
    sector = unpack_from('<H', data, i * 2)[0]
    if sector == 0:
      break
    toc.append(sector)

  entry_count = len(toc)
  print(f'Archive contains {entry_count} entries')
  output_path.mkdir(parents=True, exist_ok=True)

  for i in range(entry_count):
    start = toc[i] * SECTOR_SIZE
    if i < entry_count - 1:
      end = toc[i + 1] * SECTOR_SIZE
    else:
      end = len(data)

    file_path = output_path / f'event_{i:03d}.p1evt'
    print(f'Writing {file_path}')
    file_path.write_bytes(data[start:end])

def repack_event_archive(input_path: Path, archive_path: Path):
  files = glob_files_sorted(input_path, '*.p1evt', True)
  blobs: list[bytes] = []
  for file in files:
     blobs.append(Path(file).read_bytes())

  entry_count = len(blobs)
  toc_size = (entry_count + 1) * 2
  toc_sector_count = (toc_size + SECTOR_SIZE - 1) // SECTOR_SIZE

  toc: list[int] = []
  curr_sector = toc_sector_count
  for blob in blobs:
    toc.append(curr_sector)
    curr_sector += (len(blob) + SECTOR_SIZE - 1) // SECTOR_SIZE
  toc.append(0)

  data = bytearray()
  for entry in toc:
    data += pack('<H', entry)
  pad_to_sector(data)

  for blob in blobs:
    data += blob
    pad_to_sector(data)

  archive_path.write_bytes(data)
