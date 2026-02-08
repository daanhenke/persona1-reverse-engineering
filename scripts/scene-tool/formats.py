"""
Binary format definitions for Persona 1 (PS1) scene archives.
"""

# Constants
SECTOR_SIZE = 2048
PS1_BASE = 0x80100000
PS1_START = 0x80100008

# Archive entry counts
ARCHIVE_ENTRY_COUNTS = {
    "E0": 225,
    "E1": 225,
    "E2": 241,
    "E3": 129,
}

# Scene structure offsets
PTR_TABLE_OFF = 0x3C
PTR_TABLE_CNT = 9
EXT_FIELD_OFF = PTR_TABLE_OFF + PTR_TABLE_CNT * 4  # 0x60
HEADER_OFF = 0x08
HEADER_U16_CNT = 26
WORK_DATA_OFF = 0x9C
WORK_DATA_LEN = 0xCC8 - 0x9C
TILEMAP_OFF = 0xCC8
TILEMAP_LEN = 0x400
RECORDS_OFF = 0x10C8

# Header field names
HEADER_NAMES = [
    "type_id", "bgm_id", "alt_bgm_id",
    "gfx1_flag", "gfx1_default", "gfx1_alt",
    "gfx2_flag", "gfx2_default", "gfx2_alt",
    "gfx3_flag", "gfx3_default", "gfx3_alt",
    "gfx4_flag", "gfx4_default", "gfx4_alt",
    "gfx5", "gfx6",
    "field_17", "field_18", "field_19", "field_20", "field_21",
    "bg_flag", "bg_default", "bg_alt",
    "field_25",
]

# Script command sizes
CMD_SIZES = {
    0x20: 4, 0x21: 4, 0x22: 8, 0x23: 8, 0x24: 4, 0x25: 4, 0x26: 8,
    0x27: 4, 0x28: 4, 0x29: 8, 0x2A: 4, 0x2B: 8, 0x2C: 8,
    0x2D: 4, 0x2E: 8, 0x2F: 8, 0x30: 4, 0x31: 4, 0x32: 4,
    0x33: 4, 0x34: 4, 0x35: 4, 0x36: 4, 0x37: 8, 0x38: 12,
    0x39: 4, 0x3A: 4, 0x3B: 4, 0x3C: 8, 0x3D: 8, 0x3E: 12,
    0x3F: 8, 0x40: 8, 0x41: 4, 0x42: 4, 0x43: 4, 0x44: 4,
    0x45: 4, 0x46: 4, 0x47: 4, 0x48: 4, 0x49: 12, 0x4A: 8,
    0x4B: 4, 0x4C: 4, 0x4D: 4, 0x4E: 4, 0x4F: 4, 0x50: 4,
    0x51: 4, 0x52: 4, 0x53: 4, 0x54: 8, 0x55: 8, 0x56: 4,
    0x57: 4, 0x58: 8, 0x59: 4, 0x5A: 4, 0x60: 4, 0x61: 4,
    0x63: 4, 0x64: 12, 0x65: 12, 0x66: 4, 0x67: 4, 0x68: 4,
    0x69: 4, 0x6C: 4, 0x6D: 4, 0x6E: 8, 0x71: 4, 0x72: 4,
    0x73: 4, 0x74: 4, 0x75: 4, 0x76: 4, 0x77: 4, 0x78: 4,
    0x79: 8, 0x7A: 4, 0x7B: 4, 0x7C: 8, 0x80: 4, 0x81: 4,
    0x87: 8, 0x88: 4, 0x89: 4, 0x8A: 4, 0x8B: 4, 0x8C: 4,
    0x8D: 4, 0x8E: 4, 0x8F: 4
}

# Script command names
CMD_NAMES = {
    0x20: "NOP", 0x21: "END_SCRIPT", 0x22: "GOTO", 0x23: "RANDOM_BRANCH",
    0x24: "SET_FLAG", 0x25: "CLEAR_FLAG", 0x26: "CHECK_FLAG",
    0x27: "SET_ENCOUNTER", 0x28: "SET_NEXT_SIMPLE", 0x29: "SET_EVENT",
    0x2A: "START_BATTLE", 0x2B: "SET_NEXT_EVENT", 0x2C: "SET_EVENT_ALT",
    0x2D: "SET_MOVIE", 0x2E: "CHECK_NAME", 0x2F: "CHECK_LEVEL",
    0x30: "CHECK_MEMBER", 0x31: "ADD_MEMBER", 0x32: "REMOVE_MEMBER",
    0x33: "SET_POSITION", 0x34: "CHECK_POSITION", 0x35: "SET_PARTY_35",
    0x36: "CHECK_PROTAG", 0x37: "CHECK_MEMBER_COUNT", 0x38: "CHECK_EXP",
    0x39: "REMOVE_PERSONA", 0x3A: "CHECK_EQUIP", 0x3B: "CHECK_ITEM_99",
    0x3C: "ADD_ITEM", 0x3D: "REMOVE_ITEM", 0x3E: "CHECK_MONEY",
    0x3F: "MODIFY_MONEY", 0x40: "CHECK_PROTAG_LV",
    0x41: "SET_41", 0x42: "DAMAGE_HP", 0x43: "DAMAGE_SP",
    0x44: "RESTORE_HP", 0x45: "RESTORE_SP",
    0x46: "CHECK_PERSONA_TYPE", 0x47: "SET_PERSONA_TYPE",
    0x48: "CHECK_PERSONA_MATCH", 0x49: "CHECK_PERSONA_SPELL",
    0x4A: "SET_PERSONA_SPELL", 0x4B: "CASINO_GAME", 0x4C: "VELVET_ROOM",
    0x4D: "WAIT", 0x4E: "CHECK_ALIVE", 0x4F: "NEGOTIATE",
    0x50: "CHECK_PERSONA", 0x51: "CHECK_SLOT_PERSONA",
    0x52: "CLEAR_PERSONA_SLOT", 0x53: "CMD_53", 0x54: "ASK",
    0x55: "DIALOGUE", 0x56: "PLAY_SOUND", 0x57: "SET_57", 0x58: "SET_58",
    0x59: "CHECK_59", 0x5A: "CHECK_NEGOTIATE",
    0x60: "INIT_TEXTBOX", 0x61: "CLOSE_TEXTBOX", 0x63: "SET_BG",
    0x64: "SETUP_SPRITE", 0x65: "SETUP_SPRITE_ALT", 0x66: "HIDE_SPRITE",
    0x67: "LOAD_PORTRAIT", 0x68: "CLEAR_PORTRAIT", 0x69: "SHOW_EMOTION",
    0x6C: "SETUP_ANIM", 0x6D: "CLEAR_ANIM", 0x6E: "SETUP_EFFECT",
    0x71: "SETUP_SCROLL", 0x72: "CLEAR_SCROLL",
    0x73: "SET_FLAG_200", 0x74: "CLEAR_FLAG_200",
    0x75: "SPRITE_FLIP_ON", 0x76: "SPRITE_FLIP_ON2", 0x77: "SPRITE_FLIP_OFF",
    0x78: "WALK_TO", 0x79: "SETUP_CHARS", 0x7A: "FINALIZE_OFFSET",
    0x7B: "WAIT_WALK_STOP", 0x7C: "UPDATE_CHAR_POS",
    0x80: "PLAY_BGM", 0x81: "PLAY_SFX",
    0x87: "CHECK_DATE", 0x88: "DISABLE_CALENDAR",
    0x89: "ENABLE_CALENDAR", 0x8A: "RESET_DATE",
}

# Commands with branch targets (offset within command bytes where pointer is)
CMD_BRANCH_OFFSETS = {
    0x22: 4, 0x23: 4, 0x26: 4, 0x2E: 4, 0x2F: 4,
    0x37: 4, 0x38: 8, 0x3E: 8, 0x40: 4, 0x49: 8,
    0x54: 4, 0x87: 4,
}

DIALOGUE_OP = 0x55
DIALOGUE_PTR = 4

# Text control codes
TEXT_CONTROLS = {
    0x00: "END1", 0x01: "CLOSE", 0x02: "END2", 0x03: "LF",
    0x04: "CLR", 0x05: "PAGE", 0x06: "COLOR", 0x07: "SPEED",
    0x08: "WAIT", 0x09: "OPTS", 0x0A: "OPT", 0x0B: "OPTE",
    0x0C: "AUTO", 0x0D: "PAUSE", 0x0E: "CHC", 0x0F: "NAME",
    0x10: "CMD10", 0x11: "CMD11", 0x12: "CMD12", 0x13: "CMD13",
}

TEXT_TERMINATORS = {0x01}
TEXT_CONTROL_PARAMS = {0x06: 1, 0x07: 1, 0x08: 2}


def ptr2off(ptr):
    """Convert PS1 RAM pointer to file offset."""
    return (ptr - PS1_BASE) + 8


def off2ptr(off):
    """Convert file offset to PS1 RAM pointer."""
    return (off - 8) + PS1_BASE


def is_ptr(v):
    """Check if value looks like a valid PS1 RAM pointer."""
    return PS1_BASE <= v < PS1_BASE + 0x100000
