class AbstractConfig:
    """Абстрактный класс для работы с конфиг файлами."""

    def load_config_file(self, file):
        """
        Загружает данные из файла и возвращает экземпляр
        класса для работы с данными.
        """

    @property
    def config(self):
        """Возвращает экземпляр для работы с данными из конфиг файла."""
        return self._config

    def __init__(self, config_file):
        """Загружает данные из конфиг файла."""
        self._config = self.load_config_file(config_file)

    def __getitem__(self, item):
        return self.config[item]

    def __repr__(self):
        return self.config
