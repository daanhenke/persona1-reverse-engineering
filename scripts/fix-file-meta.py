#!/usr/bin/env python3
from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

SECTOR_2352 = 2352
USER_OFF = 24
USER_LEN = 2048
PVD_LBA = 16


@dataclass(frozen=True)
class IsoEntry:
    lba: int
    size: int
    is_dir: bool


def norm_key(s: str) -> str:
    s = s.strip().replace("\\", "/")
    s = s.split(";", 1)[0]
    s = s.lstrip("/")
    return ("/" + s).upper()


def _u32_le(b: bytes, off: int) -> int:
    return int.from_bytes(b[off:off + 4], "little")


class BinIso:
    def __init__(self, bin_path: Path):
        self.bin_path = bin_path

    def read_user(self, lba: int, nbytes: int) -> bytes:
        if nbytes <= 0:
            return b""
        with self.bin_path.open("rb") as f:
            f.seek(lba * SECTOR_2352 + USER_OFF)
            out = bytearray()
            remain = nbytes
            cur_lba = lba
            while remain > 0:
                f.seek(cur_lba * SECTOR_2352 + USER_OFF)
                chunk = f.read(USER_LEN)
                if len(chunk) != USER_LEN:
                    raise IOError("Unexpected EOF reading BIN")
                take = min(USER_LEN, remain)
                out.extend(chunk[:take])
                remain -= take
                cur_lba += 1
            return bytes(out)

    def write_user_inplace(self, lba: int, data: bytes, extent_size: int) -> None:
        if len(data) > extent_size:
            raise ValueError(f"new data {len(data)} > file size {extent_size}")
        pad = extent_size - len(data)
        payload = data + (b"\x00" * pad)
        with self.bin_path.open("r+b") as f:
            remain = len(payload)
            idx = 0
            cur_lba = lba
            while remain > 0:
                f.seek(cur_lba * SECTOR_2352 + USER_OFF)
                take = min(USER_LEN, remain)
                f.write(payload[idx:idx + take])
                idx += take
                remain -= take
                cur_lba += 1

    def pvd_ok(self) -> bool:
        pvd = self.read_user(PVD_LBA, USER_LEN)
        return len(pvd) == USER_LEN and pvd[1:6] == b"CD001"


def scan_extents(img: BinIso) -> Dict[str, IsoEntry]:
    if not img.pvd_ok():
        raise ValueError("BIN does not look like ISO9660 in MODE2 user data (missing CD001 PVD)")

    pvd = img.read_user(PVD_LBA, USER_LEN)
    root_rec = pvd[156:156 + 34]
    root_lba = _u32_le(root_rec, 2)
    root_size = _u32_le(root_rec, 10)

    out: Dict[str, IsoEntry] = {}

    def read_dir(lba: int, size: int) -> bytes:
        return img.read_user(lba, size)

    def parse_dir(lba: int, size: int, parent: str) -> None:
        buf = read_dir(lba, size)
        i = 0
        while i < len(buf):
            rec_len = buf[i]
            if rec_len == 0:
                i = ((i // USER_LEN) + 1) * USER_LEN
                continue
            rec = buf[i:i + rec_len]
            i += rec_len

            extent_lba = _u32_le(rec, 2)
            data_len = _u32_le(rec, 10)
            is_dir = (rec[25] & 0x02) != 0

            name_len = rec[32]
            name_bytes = rec[33:33 + name_len]
            if name_len == 1 and name_bytes in (b"\x00", b"\x01"):
                continue

            name = name_bytes.decode("ascii", errors="replace")
            name_nover = name.split(";", 1)[0]
            full = (parent.rstrip("/") + "/" + name_nover) if parent != "/" else ("/" + name_nover)
            key = full.upper()
            out[key] = IsoEntry(extent_lba, data_len, is_dir)
            if is_dir:
                parse_dir(extent_lba, data_len, full)

    parse_dir(root_lba, root_size, "/")
    return out


def read_fname_dat(img: BinIso, extents: Dict[str, IsoEntry], fname_path: str) -> List[str]:
    ent = extents.get(norm_key(fname_path))
    if ent is None or ent.is_dir:
        raise KeyError(f"FNAME not found: {fname_path}")
    data = img.read_user(ent.lba, ent.size)
    parts = data.split(b"\x00")
    return [p.decode("ascii", errors="strict") for p in parts if p]


def pack_u32(values: List[int]) -> bytes:
    return struct.pack("<" + "I" * len(values), *values)


def patch_tables(bin_path: Path, fname: str, fsect: str, fsize: str, preview: int) -> None:
    img = BinIso(bin_path)
    ext = scan_extents(img)

    names = read_fname_dat(img, ext, fname)
    sects: List[int] = []
    sizes: List[int] = []
    missing = 0

    for n in names:
        ent = ext.get(norm_key(n))
        if ent is None or ent.is_dir:
            sects.append(0)
            sizes.append(0)
            missing += 1
        else:
            sects.append(ent.lba)
            sizes.append(ent.size)

    fsect_ent = ext.get(norm_key(fsect))
    fsize_ent = ext.get(norm_key(fsize))
    if fsect_ent is None or fsect_ent.is_dir:
        raise KeyError(f"FSECT not found: {fsect}")
    if fsize_ent is None or fsize_ent.is_dir:
        raise KeyError(f"FSIZE not found: {fsize}")

    img.write_user_inplace(fsect_ent.lba, pack_u32(sects), fsect_ent.size)
    img.write_user_inplace(fsize_ent.lba, pack_u32(sizes), fsize_ent.size)

    print(f"patched {bin_path.name}: {len(names)} entries ({missing} missing)")
    for i in range(min(preview, len(names))):
        print(f"{i:5d} {sects[i]:8d} {sizes[i]:8d} {names[i]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Patch FSECT/FSIZE inside MODE2/2352 cue+bin (in-place).")
    ap.add_argument("cue", help="Path to .cue (used to find .bin)")
    ap.add_argument("--bin", dest="bin_path", default=None, help="Optional explicit .bin path")
    ap.add_argument("--fname", default="/FNAME.DAT")
    ap.add_argument("--fsect", default="/FSECT.DAT")
    ap.add_argument("--fsize", default="/FSIZE.DAT")
    ap.add_argument("--preview", type=int, default=20)
    args = ap.parse_args()

    cue_path = Path(args.cue).resolve()
    if not cue_path.is_file():
        print(f"not found: {cue_path}")
        return 2

    if args.bin_path:
        bin_path = Path(args.bin_path).resolve()
    else:
        bin_path = cue_path.with_suffix(".bin").resolve()

    if not bin_path.is_file():
        print(f"not found: {bin_path}")
        return 2

    try:
        patch_tables(bin_path, args.fname, args.fsect, args.fsize, args.preview)
    except Exception as e:
        print(f"error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
