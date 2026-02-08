"""
Scene parsing and building.
"""

import json
import struct
from pathlib import Path
from collections import OrderedDict

from formats import *
from script import trace_script, format_command, parse_command
from message import decode_text, encode_text


class Scene:
    """Represents a single scene entry."""

    def __init__(self):
        self.raw = b""
        self.original_size = 0
        self.prefix_ptr2 = 0x8010259C
        self.header = OrderedDict()
        self.ptr_table = []
        self.scene_data = OrderedDict()
        self.extra_script_ptrs = []
        self.work_data = b""
        self.tilemap = b""
        self.records = {}
        self.scripts = OrderedDict()  # name -> list of (offset, opcode, bytes)
        self.script_labels = OrderedDict()  # script_name -> {label_name -> command_index}
        self.messages = OrderedDict()  # id -> (offset, text, raw_bytes)

    @staticmethod
    def parse(raw_data):
        """Parse a scene from raw binary data."""
        scene = Scene()
        scene.raw = raw_data

        if len(raw_data) < RECORDS_OFF:
            return None

        # Validate header
        p1 = struct.unpack_from("<I", raw_data, 0)[0]
        if p1 != PS1_START:
            return None

        # Store prefix_ptr2
        scene.prefix_ptr2 = struct.unpack_from("<I", raw_data, 4)[0]

        # Parse header
        for i in range(HEADER_U16_CNT):
            name = HEADER_NAMES[i] if i < len(HEADER_NAMES) else f"field_{i:02d}"
            scene.header[name] = struct.unpack_from("<H", raw_data, HEADER_OFF + i * 2)[0]

        # Parse pointer table
        scene.ptr_table = [struct.unpack_from("<I", raw_data, PTR_TABLE_OFF + i * 4)[0] for i in range(PTR_TABLE_CNT)]

        # Parse scene data
        scene.scene_data["facing"] = raw_data[0x60]
        scene.scene_data["allowed_dirs"] = raw_data[0x61]
        scene.scene_data["map_width"] = raw_data[0x62]
        scene.scene_data["map_height"] = raw_data[0x63]
        scene.scene_data["map_color"] = raw_data[0x64]
        ms_ptr = struct.unpack_from("<I", raw_data, 0x68)[0]
        scene.scene_data["main_script_ptr"] = ms_ptr
        scene.scene_data["encounter_id"] = struct.unpack_from("<H", raw_data, 0x6C)[0]
        scene.scene_data["alt_encounter"] = struct.unpack_from("<H", raw_data, 0x6E)[0]
        scene.scene_data["encounter_params"] = struct.unpack_from("<H", raw_data, 0x70)[0]
        scene.scene_data["encounter_x"] = raw_data[0x72]
        scene.scene_data["encounter_y"] = raw_data[0x73]
        scene.scene_data["encounter_w"] = raw_data[0x74]
        scene.scene_data["encounter_h"] = raw_data[0x75]

        # Parse extra script pointers
        scene.extra_script_ptrs = []
        for off in range(0x78, 0x9C, 4):
            scene.extra_script_ptrs.append(struct.unpack_from("<I", raw_data, off)[0])

        # Extract work data and tilemap
        scene.work_data = raw_data[WORK_DATA_OFF:WORK_DATA_OFF + WORK_DATA_LEN]
        scene.tilemap = raw_data[TILEMAP_OFF:TILEMAP_OFF + TILEMAP_LEN]

        # Use pointer table
        ptrs = scene.ptr_table

        # Parse record tables
        record_script_ptrs = OrderedDict()
        scene.records = scene._parse_records(raw_data, ptrs, record_script_ptrs)

        # Collect script entry points
        script_entries = OrderedDict()

        # Main script
        if ms_ptr != 0xFFFFFFFF and is_ptr(ms_ptr):
            soff = ptr2off(ms_ptr)
            if RECORDS_OFF <= soff < len(raw_data):
                script_entries["main"] = soff

        # Extra scripts
        extra_ptrs = []
        for off in range(0x78, 0x9C, 4):
            extra_ptrs.append(struct.unpack_from("<I", raw_data, off)[0])

        for pi, sp in enumerate(extra_ptrs):
            if is_ptr(sp):
                soff = ptr2off(sp)
                if RECORDS_OFF <= soff < len(raw_data):
                    script_entries[f"extra_{pi}"] = soff

        # NPC work data scripts
        for off in range(WORK_DATA_OFF, WORK_DATA_OFF + WORK_DATA_LEN - 3, 4):
            v = struct.unpack_from("<I", raw_data, off)[0]
            if is_ptr(v):
                soff = ptr2off(v)
                if RECORDS_OFF <= soff < len(raw_data):
                    work_idx = (off - WORK_DATA_OFF) // 0x120
                    work_sub = (off - WORK_DATA_OFF) % 0x120
                    script_entries[f"npc{work_idx}_w{work_sub:03X}"] = soff

        # Record scripts
        for name, soff in record_script_ptrs.items():
            script_entries[name] = soff

        # Trace all scripts
        all_traced_offsets = set()
        for sname, soff in sorted(script_entries.items(), key=lambda x: x[1]):
            if soff in all_traced_offsets:
                continue
            cmds = trace_script(raw_data, soff)
            if cmds:
                scene.scripts[sname] = cmds
                for off, (op, cb) in cmds:
                    all_traced_offsets.add(off)

        # Collect messages
        msg_offsets = set()
        for sname, cmds in scene.scripts.items():
            for off, (op, cb) in cmds:
                if op == DIALOGUE_OP and len(cb) >= 8:
                    mp = struct.unpack_from("<I", cb, DIALOGUE_PTR)[0]
                    if is_ptr(mp):
                        msg_offsets.add(ptr2off(mp))

        sorted_msgs = sorted(msg_offsets)
        for mi, moff in enumerate(sorted_msgs):
            if moff >= len(raw_data):
                continue
            nxt = sorted_msgs[mi + 1] if mi + 1 < len(sorted_msgs) else len(raw_data)
            end = moff
            while end < min(nxt, len(raw_data) - 1):
                if raw_data[end] == 0xFF and raw_data[end + 1] in TEXT_TERMINATORS:
                    end += 2
                    break
                end += 1
            else:
                end = min(moff + 512, len(raw_data))
            scene.messages[mi] = (moff, None, raw_data[moff:end])

        return scene

    def _parse_records(self, raw_data, ptrs, record_script_ptrs):
        """Parse record tables."""
        # Get counts
        counts = []
        for ci in [0, 2, 4, 6]:
            cp = ptrs[ci]
            if is_ptr(cp):
                coff = ptr2off(cp)
                counts.append(raw_data[coff] if coff < len(raw_data) else 0)
            else:
                counts.append(0)
        cnt_npc, cnt_trig, cnt_exam, cnt_exit = counts

        # Record definitions: (ptr_idx, count, record_size, name, script_ptr_offset)
        rec_defs = [
            (1, cnt_npc, 8, "npc", 4),
            (3, cnt_trig, 12, "trigger", 8),
            (5, cnt_exam, 8, "examine", 4),
            (7, cnt_exit, 14, "exit", None),
        ]

        records = {}
        for ptr_idx, count, rsz, tname, sptr_off in rec_defs:
            dp = ptrs[ptr_idx]
            recs = []
            if is_ptr(dp) and count > 0:
                base = ptr2off(dp)
                for r in range(count):
                    ro = base + r * rsz
                    if ro + rsz > len(raw_data):
                        break
                    rec = raw_data[ro : ro + rsz]
                    recs.append(rec)
                    if sptr_off is not None and sptr_off + 4 <= rsz:
                        sp = struct.unpack_from("<I", rec, sptr_off)[0]
                        if is_ptr(sp):
                            soff = ptr2off(sp)
                            if RECORDS_OFF <= soff < len(raw_data):
                                record_script_ptrs[f"{tname}_{r}"] = soff
            records[tname] = recs

        return records

    def extract(self, output_dir, enc=None):
        """Extract scene to directory with editable files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        metadata = {
            "original_size": len(self.raw) if self.raw else 0,
            "prefix_ptr2": self.prefix_ptr2,
            "header": {k: v for k, v in self.header.items()},
            "ptr_table": self.ptr_table,
            "scene": {k: v for k, v in self.scene_data.items()},
            "extra_script_ptrs": self.extra_script_ptrs,
            "records": self._export_records(),
        }
        with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Save work data and tilemap as binary blobs
        with open(output_dir / "work_data.bin", "wb") as f:
            f.write(self.work_data)
        with open(output_dir / "tilemap.bin", "wb") as f:
            f.write(self.tilemap)

        # Save scripts/messages section for round-trip compatibility
        if self.raw and len(self.raw) > RECORDS_OFF:
            with open(output_dir / "scripts_data.bin", "wb") as f:
                f.write(self.raw[RECORDS_OFF:])

        # Save scripts
        scripts_dir = output_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        for script_name, cmds in self.scripts.items():
            self._save_script(scripts_dir / f"{script_name}.txt", cmds)

        # Save messages
        messages_dir = output_dir / "messages"
        messages_dir.mkdir(exist_ok=True)

        for msg_id, (moff, text, raw) in self.messages.items():
            if text is None and enc:
                text, _ = decode_text(raw, 0, enc)
            elif text is None:
                text, _ = decode_text(raw, 0, None)

            with open(messages_dir / f"{msg_id:03d}.txt", "w", encoding="utf-8") as f:
                f.write(text)

    def _export_records(self):
        """Export records to JSON-serializable format."""
        result = {}
        for rtype, recs in self.records.items():
            result[rtype] = [list(rec) for rec in recs]
        return result

    def _save_script(self, filepath, cmds):
        """Save a script to a text file."""
        # Build label map
        label_map = {}
        msg_label = {}

        # Add branch targets
        for off, (op, cb) in cmds:
            if op in CMD_BRANCH_OFFSETS:
                bo = CMD_BRANCH_OFFSETS[op]
                if bo + 4 <= len(cb):
                    bp = struct.unpack_from("<I", cb, bo)[0]
                    if is_ptr(bp):
                        label_map[ptr2off(bp)] = f"L_{ptr2off(bp):04X}"

        # Add message labels
        for msg_id, (moff, text, raw) in self.messages.items():
            msg_label[moff] = f"msg_{msg_id:03d}"

        # Write script
        with open(filepath, "w", encoding="utf-8") as f:
            prev_end = None
            for off, (op, cb) in cmds:
                # Add blank line if gap
                if prev_end is not None and off > prev_end:
                    f.write("\n")

                # Add label if this is a branch target
                if off in label_map:
                    f.write(f"{label_map[off]}:\n")

                # Write command
                line = format_command(op, cb, label_map, msg_label)
                f.write(f"    {line}\n")
                prev_end = off + len(cb)

    @staticmethod
    def load(input_dir, enc=None):
        """Load scene from extracted directory."""
        input_dir = Path(input_dir)
        scene = Scene()

        # Load metadata
        with open(input_dir / "metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

        scene.original_size = metadata.get("original_size", 0)
        scene.prefix_ptr2 = metadata.get("prefix_ptr2", 0x8010259C)
        scene.header = OrderedDict(metadata["header"])
        scene.ptr_table = metadata.get("ptr_table", [])
        scene.scene_data = OrderedDict(metadata["scene"])
        scene.extra_script_ptrs = metadata.get("extra_script_ptrs", [])
        scene.records = {}
        for rtype, recs in metadata["records"].items():
            scene.records[rtype] = [bytes(rec) for rec in recs]

        # Load work data and tilemap
        with open(input_dir / "work_data.bin", "rb") as f:
            scene.work_data = f.read()
        with open(input_dir / "tilemap.bin", "rb") as f:
            scene.tilemap = f.read()

        # Load scripts/messages section for round-trip
        scripts_data_file = input_dir / "scripts_data.bin"
        if scripts_data_file.exists():
            # Rebuild raw by combining fixed and variable sections
            raw = bytearray(RECORDS_OFF)
            # We'll fill in the header etc. during build()
            with open(scripts_data_file, "rb") as f:
                raw.extend(f.read())
            scene.raw = bytes(raw)

        # Load scripts
        scripts_dir = input_dir / "scripts"
        if scripts_dir.exists():
            for script_file in sorted(scripts_dir.glob("*.txt")):
                script_name = script_file.stem
                commands, labels = scene._load_script(script_file)
                scene.scripts[script_name] = commands
                scene.script_labels[script_name] = labels

        # Load messages
        messages_dir = input_dir / "messages"
        if messages_dir.exists():
            for msg_file in sorted(messages_dir.glob("*.txt")):
                msg_id = int(msg_file.stem)
                with open(msg_file, "r", encoding="utf-8") as f:
                    text = f.read()
                if enc:
                    raw = encode_text(text, enc)
                else:
                    raw = b""  # Will need to handle this
                scene.messages[msg_id] = (0, text, raw)

        return scene

    def _load_script(self, filepath):
        """Load a script from a text file, returning (commands, labels)."""
        commands = []
        labels = {}  # label_name -> index in commands list
        line_num = 0

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                line_num += 1

                # Skip empty lines
                if not line.strip():
                    continue

                # Check for label
                if line.endswith(":") and not line.strip().startswith(" "):
                    label_name = line[:-1].strip()
                    labels[label_name] = len(commands)
                    continue

                # Parse command
                if line.strip():
                    result = parse_command(line)
                    if result:
                        commands.append(result)

        return (commands, labels)

    def build(self):
        """Build binary scene data from components with full script/message rebuilding."""
        # Start with fixed header section
        data = bytearray(RECORDS_OFF)

        # Write magic values
        struct.pack_into("<I", data, 0, PS1_START)
        struct.pack_into("<I", data, 4, self.prefix_ptr2)

        # Write header (will update pointers later)
        for i, (name, val) in enumerate(self.header.items()):
            struct.pack_into("<H", data, HEADER_OFF + i * 2, val)

        # Placeholder for pointer table (will update later)
        for i in range(PTR_TABLE_CNT):
            struct.pack_into("<I", data, PTR_TABLE_OFF + i * 4, 0)

        # Write scene data (will update script pointer later)
        data[0x60] = self.scene_data.get("facing", 0)
        data[0x61] = self.scene_data.get("allowed_dirs", 0)
        data[0x62] = self.scene_data.get("map_width", 0)
        data[0x63] = self.scene_data.get("map_height", 0)
        data[0x64] = self.scene_data.get("map_color", 0)
        struct.pack_into("<I", data, 0x68, 0xFFFFFFFF)  # Will update
        struct.pack_into("<H", data, 0x6C, self.scene_data.get("encounter_id", 0))
        struct.pack_into("<H", data, 0x6E, self.scene_data.get("alt_encounter", 0))
        struct.pack_into("<H", data, 0x70, self.scene_data.get("encounter_params", 0))
        data[0x72] = self.scene_data.get("encounter_x", 0)
        data[0x73] = self.scene_data.get("encounter_y", 0)
        data[0x74] = self.scene_data.get("encounter_w", 0)
        data[0x75] = self.scene_data.get("encounter_h", 0)

        # Placeholder for extra script pointers
        for i in range(len(self.extra_script_ptrs)):
            struct.pack_into("<I", data, 0x78 + i * 4, 0)

        # Work data and tilemap
        data[WORK_DATA_OFF:WORK_DATA_OFF + len(self.work_data)] = self.work_data
        data[TILEMAP_OFF:TILEMAP_OFF + len(self.tilemap)] = self.tilemap

        # Now build variable section: records, scripts, and messages
        var_data = bytearray()
        script_offsets = {}  # script_name -> offset in file
        label_offsets = {}  # label_name -> offset in file (including intra-script labels)
        message_offsets = {}  # msg_id -> offset in file

        # Calculate record table size first (without script pointers resolved)
        temp_record_data, _ = self._build_records(RECORDS_OFF, None)
        current_offset = RECORDS_OFF + len(temp_record_data)

        # First pass: assign offsets to all scripts, their internal labels, and messages
        for script_name in self.scripts.keys():
            script_offsets[script_name] = current_offset
            label_offsets[script_name] = current_offset  # Script entry point is also a label
            
            cmds = self.scripts[script_name]
            script_labels = self.script_labels.get(script_name, {})
            
            # Build label offset map for this script
            # Map each label name to its absolute file offset
            if isinstance(cmds, list) and len(cmds) > 0:
                # Calculate offset of each command within the script
                cmd_offsets = {}  # cmd_index -> offset within script
                relative_offset = 0
                for cmd_idx in range(len(cmds)):
                    cmd_offsets[cmd_idx] = relative_offset
                    # Get command bytes
                    if isinstance(cmds[cmd_idx], tuple) and len(cmds[cmd_idx]) >= 2:
                        if len(cmds[cmd_idx]) == 3:
                            # Format: (opcode, bytes, label_refs)
                            opcode, cb, label_refs = cmds[cmd_idx]
                            relative_offset += len(cb)
                        else:
                            # Format: (offset, (opcode, bytes))
                            off, (op, cb) = cmds[cmd_idx]
                            relative_offset += len(cb)
                
                # Now map script labels to absolute offsets
                for label_name, cmd_idx in script_labels.items():
                    if cmd_idx in cmd_offsets:
                        abs_offset = current_offset + cmd_offsets[cmd_idx]
                        label_offsets[label_name] = abs_offset
                
                current_offset += relative_offset

        # Assign offsets to messages
        for msg_id in sorted(self.messages.keys()):
            message_offsets[msg_id] = current_offset
            label_offsets[f"msg_{msg_id:03d}"] = current_offset
            moff, text, raw = self.messages[msg_id]
            current_offset += len(raw)

        # Now rebuild record tables with resolved script pointers
        record_data, record_ptrs = self._build_records(RECORDS_OFF, script_offsets)
        var_data.extend(record_data)

        # Second pass: build scripts with resolved label pointers
        script_data = bytearray()
        for script_name, cmds in self.scripts.items():
            if isinstance(cmds, list) and len(cmds) > 0 and isinstance(cmds[0], tuple):
                if len(cmds[0]) == 3:
                    # Commands from loading (opcode, bytes, label_refs)
                    for opcode, cb, label_refs in cmds:
                        cb_copy = bytearray(cb)
                        # Resolve label references
                        for offset_in_cmd, label_name in label_refs.items():
                            if label_name in label_offsets:
                                target_off = label_offsets[label_name]
                                target_ptr = off2ptr(target_off)
                                struct.pack_into("<I", cb_copy, offset_in_cmd, target_ptr)
                        script_data.extend(cb_copy)
                else:
                    # Commands from parsing (offset, (opcode, bytes))
                    for off, (op, cb) in cmds:
                        script_data.extend(cb)

        var_data.extend(script_data)

        # Add messages
        for msg_id in sorted(self.messages.keys()):
            moff, text, raw = self.messages[msg_id]
            var_data.extend(raw)

        # Update pointer table with record pointers
        for i, ptr in enumerate(record_ptrs):
            if ptr != 0:
                struct.pack_into("<I", data, PTR_TABLE_OFF + i * 4, ptr)

        # Update main script pointer
        if "main" in script_offsets:
            struct.pack_into("<I", data, 0x68, off2ptr(script_offsets["main"]))

        # Update extra script pointers
        extra_names = [f"extra_{i}" for i in range(len(self.extra_script_ptrs))]
        for i, name in enumerate(extra_names):
            if name in script_offsets:
                struct.pack_into("<I", data, 0x78 + i * 4, off2ptr(script_offsets[name]))

        # Update NPC work data script pointers
        work_data_copy = bytearray(self.work_data)
        for off in range(0, len(work_data_copy) - 3, 4):
            work_idx = off // 0x120
            work_sub = off % 0x120
            script_name = f"npc{work_idx}_w{work_sub:03X}"
            if script_name in script_offsets:
                struct.pack_into("<I", work_data_copy, off, off2ptr(script_offsets[script_name]))
        data[WORK_DATA_OFF:WORK_DATA_OFF + len(work_data_copy)] = work_data_copy

        # Combine all sections
        data.extend(var_data)

        # Pad to sector boundary
        while len(data) % SECTOR_SIZE != 0:
            data.append(0)

        # Pad to original size if we have it
        if self.original_size > 0 and len(data) < self.original_size:
            while len(data) < self.original_size:
                data.append(0)

        return bytes(data)

    def _build_records(self, base_offset, script_offsets=None):
        """Build record tables and return (data, pointer_list)."""
        record_data = bytearray()
        pointers = [0] * PTR_TABLE_CNT

        # Get record counts
        counts = []
        for rtype in ["npc", "trigger", "examine", "exit"]:
            counts.append(len(self.records.get(rtype, [])))
        cnt_npc, cnt_trig, cnt_exam, cnt_exit = counts

        # Record definitions: (count_idx, data_idx, count, records, record_size, name, script_ptr_offset)
        rec_defs = [
            (0, 1, cnt_npc, self.records.get("npc", []), 8, "npc", 4),
            (2, 3, cnt_trig, self.records.get("trigger", []), 12, "trigger", 8),
            (4, 5, cnt_exam, self.records.get("examine", []), 8, "examine", 4),
            (6, 7, cnt_exit, self.records.get("exit", []), 14, "exit", None),
        ]

        current_offset = base_offset
        for count_idx, data_idx, count, recs, rsz, tname, sptr_off in rec_defs:
            if count > 0:
                # Write count
                pointers[count_idx] = off2ptr(current_offset)
                record_data.append(count)
                current_offset += 1

                # Write records
                pointers[data_idx] = off2ptr(current_offset)
                for rec_idx, rec in enumerate(recs):
                    rec_copy = bytearray(rec[:rsz])

                    # Update script pointer if this record type has one
                    if sptr_off is not None and script_offsets:
                        script_name = f"{tname}_{rec_idx}"
                        if script_name in script_offsets:
                            struct.pack_into("<I", rec_copy, sptr_off, off2ptr(script_offsets[script_name]))

                    record_data.extend(rec_copy)
                current_offset += count * rsz

        return record_data, pointers