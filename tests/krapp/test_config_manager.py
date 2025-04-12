import json
import os
import sys
from pathlib import Path

import pytest

from krapp.config_manager import ConfigManager


@pytest.fixture
def config_manager():
    return ConfigManager()


# def test_config_file_windows(monkeypatch, config_manager):
#     monkeypatch.setattr(os, "name", "nt")
#     monkeypatch.setenv("APPDATA", "C:\\Users\\TestUser\\AppData\\Roaming")
#     expected_path = Path("C:\\Users\\TestUser\\AppData\\Roaming\\krapp\\config.json")
#     assert config_manager.config_file == expected_path


def test_config_file_mac(monkeypatch, config_manager):
    monkeypatch.setattr(os, "name", "posix")
    monkeypatch.setattr(sys, "platform", "darwin")
    expected_path = Path("~/Library/Application Support/krapp/config.json").expanduser()
    assert config_manager.config_file == expected_path


def test_config_file_linux(monkeypatch, config_manager):
    monkeypatch.setattr(os, "name", "posix")
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setenv("XDG_CONFIG_HOME", "/home/testuser/.config")
    expected_path = Path("/home/testuser/.config/krapp/config.json")
    assert config_manager.config_file == expected_path


def test_config_file_linux_default(monkeypatch, config_manager):
    monkeypatch.setattr(os, "name", "posix")
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    expected_path = Path("~/.config/krapp/config.json").expanduser()
    assert config_manager.config_file == expected_path



def test_set_config(config_manager):
    config_manager.set_config("max_retries", 5)
    assert config_manager.get_config("max_retries") == 5
