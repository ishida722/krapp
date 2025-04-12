import json
import os
import sys
from pathlib import Path
from typing import Any


class ConfigManager:
    @property
    def config_file(self) -> Path:
        if os.name == "nt":  # Windows
            return Path(os.getenv("APPDATA", ""), "krapp", "config.json").expanduser()
        elif os.name == "posix":  # macOS and Linux
            if sys.platform == "darwin":  # macOS
                return Path(
                    "~/Library/Application Support/krapp", "config.json"
                ).expanduser()
            else:  # Linux
                return Path(
                    os.getenv("XDG_CONFIG_HOME", "~/.config"),
                    "krapp",
                    "config.json",
                ).expanduser()

        else:
            raise NotImplementedError("Unsupported operating system")

    def __init__(self) -> None:
        self.config: dict = {
            "texts.dir": None,
        }
        self.load_config()

    def get_config(self, key) -> Any:
        return self.config.get(key, None)

    def set_config(self, key, value) -> None:
        self.config[key] = value

    def load_config(self) -> None:
        """
        Load configuration from a file.
        The file should be in JSON format.
        """

        if not self.config_file.exists():
            return

        with open(self.config_file, "r") as file:
            self.config = json.load(file)

    def save_config(self) -> None:
        """
        Save configuration to a file.
        The file will be in JSON format.
        """
        os.makedirs(self.config_file.parent, exist_ok=True)
        with open(self.config_file, "w") as file:
            json.dump(self.config, file, indent=4)
