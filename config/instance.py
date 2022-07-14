import os.path
from importlib import import_module
from pathlib import Path

from config.exceptions import UnknownFileExtension
from config.extensions import INIConfig, JSONConfig, AvailableExtensions


SomePath = Path | str
ConfigClass = JSONConfig | INIConfig


class Settings:
    """
    Класс для получения значений из файла настроек *.py и загрузки данных
    из *.ini, *.cfg, *.json файлов.
    """

    def setup_config_from_settings(self, settings_file):
        """
        Устанавливает значения из аргумента `settings_file`,
        который должен быть *.py файлом.
        """
        settings_module = import_module(settings_file)
        config_list = [
            constant for constant in dir(settings_module) if not constant.startswith('__')
        ]  # Не берёт во внимание dunder-переменные файла `settings_file`
        for constant in config_list:
            setattr(self, constant, getattr(settings_module, constant))

    def setup_config_files(self, config_files: dict[str, SomePath]):
        """Устанавливает в атрибуты класса данные из конфиг файлов."""
        for config_name, path_to_file in config_files.items():
            if not hasattr(self, config_name):
                setattr(
                    self, config_name, self.get_config_class(path_to_file)
                )
            else:
                raise AttributeError(
                    f"Атрибут `{config_name}` уже существует и имеет значение {getattr(self, config_name)}"
                )

    def get_config_class(self, path_to_file: SomePath) -> ConfigClass:
        """
        Узнаёт, какой формат имеет файл и возвращает класс, который
        сможет загрузить данные из него.
        """
        file_extension = self.get_file_extension(path_to_file)
        match file_extension:
            case AvailableExtensions.JSON:
                return JSONConfig(path_to_file)
            case AvailableExtensions.INI | AvailableExtensions.CFG:
                return INIConfig(path_to_file)

    @staticmethod
    def get_file_extension(path_to_file: SomePath) -> AvailableExtensions:
        """
        Получает разрешения файла. Если разрешение нет в
        `config.extensions.AvailableExtensions`, вызывается исключение
        `config.exceptions.UnknownFileExtension`.
        """
        config_file = os.path.basename(path_to_file)
        for extension in AvailableExtensions:
            if config_file.endswith('.' + extension.value):
                return extension
        raise UnknownFileExtension(f'Неизвестное разрешение файла `{config_file}`')

    def __init__(self, settings_file: str, config_files: dict[str, SomePath] = None):
        """
        Загружает значения и устанавливает их как атрибуты класса из
        аргумента `settings_file`, который должен быть названием *.py файла.
        Также загружает конфиг файлы, если они переданы аргументом `config_files`.
        """
        self.setup_config_from_settings(settings_file)
        if config_files:
            self.setup_config_files(config_files)
