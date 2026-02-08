"""
Script parsing and generation.
"""

import struct
from formats import (
    CMD_SIZES, CMD_NAMES, CMD_BRANCH_OFFSETS, DIALOGUE_OP, DIALOGUE_PTR,
    RECORDS_OFF, ptr2off, off2ptr, is_ptr
)


def trace_script(raw, start_off):
    """
    Parse script starting at start_off, following all branch targets.

    Returns:
        list: [(offset, opcode, cmd_bytes), ...] for all reachable code
    """
    if start_off >= len(raw) or start_off < RECORDS_OFF:
        return []

    visited = set()
    queue = [start_off]
    all_cmds = {}  # offset -> (op, bytes)

    while queue:
        pos = queue.pop(0)
        if pos in visited or pos >= len(raw) - 1 or pos < RECORDS_OFF:
            continue

        while pos < len(raw) - 1 and pos not in visited:
            visited.add(pos)
            if raw[pos] != 0xFF:
                break

            op = raw[pos + 1]
            if op not in CMD_SIZES:
                print('unknown opcode {}'.format(op))
                break

            sz = CMD_SIZES[op]
            if pos + sz > len(raw):
                break

            cb = raw[pos : pos + sz]
            all_cmds[pos] = (op, cb)

            # Follow branch targets
            if op in CMD_BRANCH_OFFSETS:
                bo = CMD_BRANCH_OFFSETS[op]
                if bo + 4 <= sz:
                    bp = struct.unpack_from("<I", cb, bo)[0]
                    if is_ptr(bp):
                        target = ptr2off(bp)
                        if target not in visited and RECORDS_OFF <= target < len(raw):
                            queue.append(target)

            if op == 0x21:  # END_SCRIPT
                break
            if op == 0x22:  # GOTO - unconditional
                bo = CMD_BRANCH_OFFSETS[0x22]
                bp = struct.unpack_from("<I", cb, bo)[0]
                if is_ptr(bp):
                    target = ptr2off(bp)
                    if target not in visited and RECORDS_OFF <= target < len(raw):
                        queue.append(target)
                break  # don't fall through after GOTO

            pos += sz

    return sorted(all_cmds.items())


def format_command(op, cb, label_map, msg_label):
    """Format a single command as text."""
    name = CMD_NAMES.get(op, f"CMD_{op:02X}")
    sz = len(cb)
    if name == 'WAIT_WALK_STOP':
      print(op, cb, sz)

    def _branch(bo):
        if bo + 4 <= sz:
            p = struct.unpack_from("<I", cb, bo)[0]
            if is_ptr(p):
                t = ptr2off(p)
                lbl = label_map.get(t, f"L_{t:04X}")
                return f" -> {lbl}"
        return ""

    def _hex_tail(start=2):
        return " ".join(f"0x{b:02X}" for b in cb[start:])

    if op == 0x21:
        return "END_SCRIPT"
    if op == 0x22:
        return f"GOTO{_branch(4)}"

    if op == 0x24:
        return f"SET_FLAG 0x{struct.unpack_from('<H', cb, 2)[0]:04X}"
    if op == 0x25:
        return f"CLEAR_FLAG 0x{struct.unpack_from('<H', cb, 2)[0]:04X}"
    if op == 0x26:
        return f"CHECK_FLAG 0x{struct.unpack_from('<H', cb, 2)[0]:04X}{_branch(4)}"

    if op == 0x29:
        eid = struct.unpack_from("<H", cb, 2)[0]
        return f"SET_EVENT 0x{eid:04X} {_hex_tail(4)}"
    if op == 0x2B:
        eid = struct.unpack_from("<H", cb, 2)[0]
        return f"SET_NEXT_EVENT 0x{eid:04X} {_hex_tail(4)}"

    if op == 0x3C:
        item = struct.unpack_from("<H", cb, 2)[0]
        return f"ADD_ITEM 0x{item:04X} {_hex_tail(4)}"
    if op == 0x3D:
        item = struct.unpack_from("<H", cb, 2)[0]
        return f"REMOVE_ITEM 0x{item:04X} {_hex_tail(4)}"
    if op == 0x3E:
        amt = struct.unpack_from("<I", cb, 4)[0]
        return f"CHECK_MONEY 0x{cb[2]:02X} 0x{cb[3]:02X} {amt}{_branch(8)}"
    if op == 0x3F:
        amt = struct.unpack_from("<I", cb, 4)[0]
        return f"MODIFY_MONEY 0x{cb[2]:02X} 0x{cb[3]:02X} {amt}"

    if op == 0x55:  # DIALOGUE
        if sz >= 8:
            mp = struct.unpack_from("<I", cb, DIALOGUE_PTR)[0]
            if is_ptr(mp):
                t = ptr2off(mp)
                lbl = msg_label.get(t, f"msg_0x{t:04X}")
                return f"DIALOGUE 0x{cb[2]:02X} 0x{cb[3]:02X} {lbl}"
        return f"DIALOGUE {_hex_tail(2)}"

    if op == 0x87:
        return f"CHECK_DATE 0x{cb[2]:02X} 0x{cb[3]:02X}{_branch(4)}"

    # Generic branch-bearing commands
    if op in CMD_BRANCH_OFFSETS:
        bo = CMD_BRANCH_OFFSETS[op]
        before = " ".join(f"0x{b:02X}" for b in cb[2:bo])
        after_end = bo + 4
        after = " ".join(f"0x{b:02X}" for b in cb[after_end:]) if after_end < sz else ""
        parts = [name]
        if before:
            parts.append(before)
        parts.append(_branch(bo).strip())
        if after:
            parts.append(after)

        return " ".join(parts)

    # Generic
    if sz > 2:
        return f"{name} {_hex_tail(2)}"
    return name


def parse_command(line):
    """
    Parse a command from text format back to binary.

    Returns:
        tuple: (opcode, bytes, label_refs) where label_refs is a dict of {offset: label_name}
    """
    line = line.strip()
    if not line:
        return None

    # Find command name
    parts = line.split()
    if not parts:
        return None

    cmd_name = parts[0]

    # Find opcode
    opcode = None
    name = None
    for op, name in CMD_NAMES.items():
        if name == cmd_name:
            opcode = op
            break

    if opcode is None:
        # Try CMD_XX format
        if cmd_name.startswith("CMD_"):
            try:
                opcode = int(cmd_name[4:], 16)
                name = cmd_name[4:]
            except ValueError:
                return None
        else:
            return None

    if opcode not in CMD_SIZES:
        return None

    sz = CMD_SIZES[opcode]
    cb = bytearray([0xFF, opcode] + [0] * (sz - 2))
    label_refs = {}

    # Parse arguments
    if opcode == 0x21:  # END_SCRIPT
        pass
    elif opcode == 0x22:  # GOTO
        if len(parts) >= 3 and parts[1] == "->":
            label_refs[4] = parts[2]
    elif opcode in [0x24, 0x25]:  # SET_FLAG, CLEAR_FLAG
        if len(parts) >= 2:
            val = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
            struct.pack_into("<H", cb, 2, val)
    elif opcode == 0x26:  # CHECK_FLAG
        if len(parts) >= 2:
            val = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
            struct.pack_into("<H", cb, 2, val)
        if len(parts) >= 4 and parts[2] == "->":
            label_refs[4] = parts[3]
    elif opcode == 0x55:  # DIALOGUE
        if len(parts) >= 4:
            cb[2] = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
            cb[3] = int(parts[2], 16) if parts[2].startswith("0x") else int(parts[2])
            label_refs[DIALOGUE_PTR] = parts[3]
    elif opcode in [0x3C, 0x3D]:  # ADD_ITEM, REMOVE_ITEM
        if len(parts) >= 2:
            val = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
            struct.pack_into("<H", cb, 2, val)
        # Parse remaining hex bytes
        idx = 4
        for i in range(2, len(parts)):
            if parts[i].startswith("0x") and idx < sz:
                cb[idx] = int(parts[i], 16)
                idx += 1
    elif opcode == 0x3F:  # MODIFY_MONEY
        if len(parts) >= 4:
            cb[2] = int(parts[1], 16) if parts[1].startswith("0x") else int(parts[1])
            cb[3] = int(parts[2], 16) if parts[2].startswith("0x") else int(parts[2])
            amt = int(parts[3])
            struct.pack_into("<I", cb, 4, amt)
    else:
        # Generic parsing - extract hex values and labels
        arg_idx = 1
        byte_idx = 2
        while arg_idx < len(parts) and byte_idx < sz:
            arg = parts[arg_idx]
            if arg == "->":
                # Branch target follows
                if arg_idx + 1 < len(parts):
                    # Find branch offset for this opcode
                    if opcode in CMD_BRANCH_OFFSETS:
                        bo = CMD_BRANCH_OFFSETS[opcode]
                        label_refs[bo] = parts[arg_idx + 1]
                    arg_idx += 2
                else:
                    arg_idx += 1
            elif arg.startswith("0x"):
                # Hex value
                val = int(arg, 16)
                if byte_idx < sz:
                    if val <= 0xFF:
                        cb[byte_idx] = val
                        byte_idx += 1
                    elif val <= 0xFFFF and byte_idx + 1 < sz:
                        struct.pack_into("<H", cb, byte_idx, val)
                        byte_idx += 2
                    elif byte_idx + 3 < sz:
                        struct.pack_into("<I", cb, byte_idx, val)
                        byte_idx += 4
                arg_idx += 1
            elif arg.isdigit():
                # Decimal value
                val = int(arg)
                if val <= 0xFF and byte_idx < sz:
                    cb[byte_idx] = val
                    byte_idx += 1
                elif val <= 0xFFFF and byte_idx + 1 < sz:
                    struct.pack_into("<H", cb, byte_idx, val)
                    byte_idx += 2
                elif byte_idx + 3 < sz:
                    struct.pack_into("<I", cb, byte_idx, val)
                    byte_idx += 4
                arg_idx += 1
            else:
                arg_idx += 1

    return (opcode, bytes(cb), label_refs)
