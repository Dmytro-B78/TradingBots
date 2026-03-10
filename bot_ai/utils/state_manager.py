# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/utils/state_manager.py
# Purpose: JSON-based state storage with atomic writes
# Format: UTF-8 without BOM
# ============================================

import json
import os

STATE_DIR = "state"
STATE_PATH = os.path.join(STATE_DIR, "state.json")

os.makedirs(STATE_DIR, exist_ok=True)


def load_state():
    """
    Loads state from JSON file.
    Returns empty dict if file missing or corrupted.
    """
    if not os.path.isfile(STATE_PATH):
        return {}

    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state: dict):
    """
    Saves state atomically:
    - writes to temporary file
    - replaces original file
    Prevents corruption on crash.
    """
    tmp_path = STATE_PATH + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    os.replace(tmp_path, STATE_PATH)
