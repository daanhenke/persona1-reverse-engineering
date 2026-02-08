"""
Message encoding and decoding.
"""

import struct
from formats import TEXT_CONTROLS, TEXT_TERMINATORS, TEXT_CONTROL_PARAMS


class Encoding:
    """Text encoding table."""

    def __init__(self):
        self.single = {}  # byte -> string
        self.double = {}  # byte -> string (for 0x80XX codes)
        self.reverse_single = {}  # string -> byte
        self.reverse_double = {}  # string -> byte

    @staticmethod
    def load(path):
        """Load encoding table from file."""
        enc = Encoding()
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n\r")
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    continue

                key, val = line.split("=", 1)
                key = key.strip()

                if len(key) == 4 and key[:2].lower() == "80":
                    # Double-byte encoding (0x80XX)
                    byte_val = int(key[2:4], 16)
                    enc.double[byte_val] = val
                    enc.reverse_double[val] = byte_val
                else:
                    # Single-byte encoding
                    byte_val = int(key, 16)
                    enc.single[byte_val] = val
                    enc.reverse_single[val] = byte_val

        return enc


def decode_text(data, offset, enc=None, max_off=None):
    """
    Decode text from binary data.

    Returns:
        tuple: (decoded_text, bytes_read)
    """
    parts = []
    pos = offset
    limit = max_off if max_off is not None else len(data)

    while pos < limit:
        b = data[pos]

        if b == 0xFF:
            # Control code
            if pos + 1 >= len(data):
                parts.append(f"[{b:02X}]")
                pos += 1
                break

            ctrl = data[pos + 1]
            if ctrl in TEXT_CONTROLS:
                name = TEXT_CONTROLS[ctrl]
                pcount = TEXT_CONTROL_PARAMS.get(ctrl, 0)

                if pcount > 0 and pos + 2 + pcount <= len(data):
                    params = data[pos + 2 : pos + 2 + pcount]
                    pstr = " ".join(f"{p:02X}" for p in params)
                    parts.append(f"[{name} {pstr}]")
                    pos += 2 + pcount
                else:
                    parts.append(f"[{name}]")
                    pos += 2

                if ctrl in TEXT_TERMINATORS:
                    break
            else:
                parts.append(f"[FF{ctrl:02X}]")
                pos += 2

        elif b == 0x80:
            # Double-byte character
            if pos + 1 >= len(data):
                parts.append(f"[{b:02X}]")
                pos += 1
                break

            second = data[pos + 1]
            if enc and second in enc.double:
                parts.append(enc.double[second])
            else:
                parts.append(f"[80{second:02X}]")
            pos += 2

        else:
            # Single-byte character
            if enc and b in enc.single:
                parts.append(enc.single[b])
            else:
                parts.append(f"[{b:02X}]")
            pos += 1

    return "".join(parts), pos - offset


def encode_text(text, enc=None):
    """
    Encode text to binary format.

    Args:
        text: String with control codes like [LF], [END], etc.
        enc: Encoding table

    Returns:
        bytes: Encoded binary data
    """
    result = bytearray()
    pos = 0

    reverse_ctrl = {v: k for k, v in TEXT_CONTROLS.items()}

    while pos < len(text):
        # Check for control codes [XXX]
        if text[pos] == '[':
            end = text.find(']', pos)
            if end != -1:
                code = text[pos+1:end]

                # Check if it's a named control code
                if code in reverse_ctrl:
                    ctrl_byte = reverse_ctrl[code]
                    result.append(0xFF)
                    result.append(ctrl_byte)

                    # Handle parameters
                    pcount = TEXT_CONTROL_PARAMS.get(ctrl_byte, 0)
                    if pcount > 0:
                        # Extract parameters from the code
                        parts = code.split()
                        if len(parts) > 1:
                            for i in range(pcount):
                                if i + 1 < len(parts):
                                    result.append(int(parts[i + 1], 16))

                    pos = end + 1
                    continue

                # Check for hex codes like [80XX] or [XX]
                if len(code) == 4 and code[:2].upper() == "80":
                    # Double-byte code [80XX]
                    result.append(0x80)
                    result.append(int(code[2:4], 16))
                    pos = end + 1
                    continue
                elif len(code) == 4 and code[:2].upper() == "FF":
                    # Control code [FFXX]
                    result.append(0xFF)
                    result.append(int(code[2:4], 16))
                    pos = end + 1
                    continue
                elif len(code) == 2:
                    # Single byte [XX]
                    result.append(int(code, 16))
                    pos = end + 1
                    continue

        # Regular character - look up in encoding table
        if enc:
            # Try to match longest string first
            matched = False
            for length in range(min(10, len(text) - pos), 0, -1):
                substr = text[pos:pos+length]
                if substr in enc.reverse_single:
                    result.append(enc.reverse_single[substr])
                    pos += length
                    matched = True
                    break
                elif substr in enc.reverse_double:
                    result.append(0x80)
                    result.append(enc.reverse_double[substr])
                    pos += length
                    matched = True
                    break

            if not matched:
                # Unknown character, skip it
                pos += 1
        else:
            # No encoding table, can't encode
            pos += 1

    return bytes(result)