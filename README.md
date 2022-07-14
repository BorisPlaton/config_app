# Класс настроек

Пакет `config` имеет класс `config.instance.Settings`, который позволяет взаимодействовать с данными из настроек проекта, что хранятся в `*.py` файле. Также можно взаимодействовать с множеством конфигурационных файлов, которые имеют следующие разрешения:
- `*.json`
- `*.ini` 
- `*.cfg`

## API
Чтоб создать экземпляр настроек класса, следует сначала создать сами данные, с которыми мы будем взаимодействовать в будущем. 
Создадим файл `settings.py` и запишем в него следующие значения:
```
SOME_INT = 1
SOME_STRING = 'str'
SOME_DICT = {'foo': 'bar'}
```
Проинициализируем класс `config.instance.Settings` с названием файла настроек:
```
from config import Settings

settings = Settings('settings')
```
Теперь мы можем обращаться к переменным из этого файла, как к атрибутам экземпляра класса:
``` 
assert settings.SOME_INT == 1  # True
assert settings.SOME_STRING == 'str'  # True
assert settings.SOME_DICT == {'foo': 'bar'}  # True
```
Создадим конфиг файлы `json_config.json`, `cfg_config.cfg` и `ini_config.ini` и заполним их:

**json_config.json**

```
{
    "first_var": 1,
    "second_var": 2
}
```
**cfg_config.cfg**
```
[CFG]
third_var=3
fourth_var=4
```
**ini_config.ini**
```
[INI]
fifth_var=5
sixth_var=6
```
Добавим их в наш экземпляр класса:
```
from pathlib import Path

settings.setup_config_files({
    'some_name_for_ini': Path(__file__).parent / 'ini_config.ini',
    'some_name_for_json': Path(__file__).parent / 'json_config.json',
    'some_name_for_cfg': Path(__file__).parent / 'cfg_config.cfg',
})
```
Теперь мы можем обращаться к данным из этих файлов следующим образом:
```
assert settings.some_name_for_ini['fifth_var'] == '5'  # True
assert settings.some_name_for_ini['sixth_var'] == '6'  # True

assert settings.some_name_for_json['first_var'] == 1  # True
assert settings.some_name_for_json['second_var'] == 2  # True

assert settings.some_name_for_cfg['third_var'] == '3'  # True
assert settings.some_name_for_cfg['fourth_var'] == '4'  # True
```
Можно всё это сделать сразу при инициализации экземпляра класса:
```
from config import Settings

settings2 = Settings(
    'settings',
    {
        'some_name_for_ini': Path(__file__).parent / 'ini_config.ini',
        'some_name_for_json': Path(__file__).parent / 'json_config.json',
        'some_name_for_cfg': Path(__file__).parent / 'cfg_config.cfg',
    }
)
```
## Тесты
Для запуска тестов введите следующее в командную строку:
```
>>> python -m unittest discover tests
```