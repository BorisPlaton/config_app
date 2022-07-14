import json
from configparser import ConfigParser
from enum import Enum

from core.abstract import AbstractConfig


class AvailableExtensions(Enum):
    """Доступные разрешения файлов."""
    JSON = 'json'
    CFG = 'cfg'
    INI = 'ini'


class JSONConfig(AbstractConfig):
    """Класс для загрузки JSON-файла, как файла конфига."""

    def load_config_file(self, json_config: str | bytes):
        with open(json_config) as config_file:
            config = json.loads(config_file.read())
        return config


class INIConfig(AbstractConfig):
    """Класс для загрузки *.ini, *.cfg файлов, как файлов конфига."""

    def load_config_file(self, file):
        config = ConfigParser()
        config.read(file)
        return config
