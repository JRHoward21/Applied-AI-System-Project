import os
import json
from datetime import datetime
from typing import Dict, List, Optional


DEFAULT_HISTORY_PATH = os.path.join("assets", "game_history.json")


def _ensure_assets_dir(path: str) -> None:
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def append_user_history(user_prefs: Dict, file_path: Optional[str] = None) -> None:
    path = file_path or DEFAULT_HISTORY_PATH
    _ensure_assets_dir(path)

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "prefs": user_prefs,
    }

    data: List[Dict] = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or []
        except Exception:
            data = []

    data.append(entry)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_user_history(file_path: Optional[str] = None) -> List[Dict]:
    path = file_path or DEFAULT_HISTORY_PATH
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except Exception:
        return []
