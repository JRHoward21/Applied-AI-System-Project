import os
import tempfile
from history import append_user_history, get_user_history


def test_append_and_read_history(tmp_path):
    fp = os.path.join(tmp_path, "history.json")
    prefs = {"system": "PC", "favorite_game": "Minecraft", "history": "building"}
    append_user_history(prefs, file_path=fp)
    h = get_user_history(file_path=fp)
    assert isinstance(h, list)
    assert h and h[-1]["prefs"]["favorite_game"] == "Minecraft"
