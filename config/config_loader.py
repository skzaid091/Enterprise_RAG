import json
import os
import tempfile

CONFIG_PATH = "config/config.json"


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def save_config(config):
    """Atomically write config so a crash can't corrupt the file."""
    dir_name = os.path.dirname(CONFIG_PATH)
    # Write to a temp file in the same directory, then rename (atomic on POSIX)
    with tempfile.NamedTemporaryFile(
        mode="w", dir=dir_name, suffix=".tmp", delete=False
    ) as tmp:
        json.dump(config, tmp, indent=4)
        tmp_path = tmp.name
    os.replace(tmp_path, CONFIG_PATH)