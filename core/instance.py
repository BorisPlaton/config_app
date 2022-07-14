import os.path
from importlib import import_module
from pathlib import Path

from core.exceptions import UnknownFileExtension
from core.extensions import INIConfig, JSONConfig, AvailableExtensions


SomePath = Path | str


class Settings:
    """Класс для получения значений из `config.settings`."""

    def setup_config_from_settings(self):
        """Устанавливает значения из `configuration.settings`."""
        config_list = [
            constant for constant in dir(self.settings_module) if not constant.startswith('__')
        ]  # Не берёт во внимание переменные файла `settings.py`, к примеру  `__file__`, `__name__` и т.д.
        for constant in config_list:
            setattr(self, constant, getattr(self.settings_module, constant))

    def setup_config_files(self, config_files: dict[str, SomePath]):
        for config_name, path_to_file in config_files.items():
            config_class = self.get_config_class(path_to_file)
            if not hasattr(self, config_name):
                setattr(self, config_name, config_class)
            else:
                raise AttributeError(
                    f"Атрибут `{config_name}` уже существует и имеет значение {getattr(self, config_name)}"
                )

    def get_config_class(self, path_to_file: SomePath) -> JSONConfig | INIConfig:
        file_extension = self.get_file_extension(path_to_file)
        match file_extension:
            case AvailableExtensions.JSON:
                return JSONConfig(path_to_file)
            case AvailableExtensions.INI | AvailableExtensions.CFG:
                return INIConfig(path_to_file)

    @staticmethod
    def get_file_extension(path_to_file: SomePath) -> AvailableExtensions:
        """
        Получает разрешения файла. Если разрешение нет в `AvailableExtensions`,
        вызывается исключение `UnknownFileExtension`.
        """
        config_file = os.path.basename(path_to_file)
        for extension in AvailableExtensions:
            if config_file.endswith('.' + extension.value):
                return extension
        raise UnknownFileExtension(f'Неизвестное разрешение файла `{config_file}`')

    def __init__(self, settings_file: str, config_files: dict[str, SomePath] = None):
        """
        Загружает значения и устанавливает их как атрибуты класса из
        `settings.py` файла. Также загружает конфиг файлы, если они переданы
        аргументом `config_files`.
        """
        self.settings_module = import_module(settings_file)
        self.setup_config_from_settings()

        if config_files:
            self.setup_config_files(config_files)
