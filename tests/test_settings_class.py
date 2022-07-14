from pathlib import Path
from unittest import TestCase

from config import UnknownFileExtension
from config import Settings
import settings_test as st


class SettingsClass(TestCase):

    def test_settings_creation_without_config_files(self):
        settings_instance = Settings('settings_test')
        self.assertEqual(st.SOME_VAR, settings_instance.SOME_VAR)
        self.assertEqual(st.dict_const, settings_instance.dict_const)
        self.assertEqual(st.another_var, settings_instance.another_var)

    def test_settings_creation_with_json_config(self):
        settings_instance = Settings('settings_test', {'test_json': Path(__file__).parent / 'test_config.json'})
        self.assertTrue(settings_instance.test_json)
        self.assertEqual(settings_instance.test_json['test_var_1'], 1)
        self.assertEqual(settings_instance.test_json['test_var_2'], 'test_var_2 value')
        self.assertEqual(settings_instance.test_json['test_var_3'], 3)
        self.assertEqual(settings_instance.test_json['dict_var']['one'], 1)
        self.assertRaises(KeyError, lambda: settings_instance.test_json['dict_var']['not existed var'])

    def test_unknown_file_extension(self):
        file_extensions = ['s', 'gg', 's', 'mp3', 'son', 'i']
        for extension in file_extensions:
            self.assertRaises(
                UnknownFileExtension, lambda: Settings(
                    'settings_test',
                    {'test_json': Path(__file__).parent / f'test_config.{extension}'}
                )
            )

    def test_settings_creation_with_json_config_and_string_path(self):
        settings_instance = Settings(
            'settings_test',
            {'test_json': str(Path(__file__).parent / 'test_config.json')}
        )
        self.assertTrue(settings_instance.test_json)
        self.assertEqual(settings_instance.test_json['test_var_1'], 1)
        self.assertEqual(settings_instance.test_json['test_var_2'], 'test_var_2 value')
        self.assertEqual(settings_instance.test_json['test_var_3'], 3)
        self.assertEqual(settings_instance.test_json['dict_var']['one'], 1)
        self.assertRaises(KeyError, lambda: settings_instance.test_json['dict_var']['not existed var'])

    def test_settings_creation_with_multiple_json_files(self):
        settings_instance = Settings(
            'settings_test',
            {
                'test_json': str(Path(__file__).parent / 'test_config.json'),
                'someatr': str(Path(__file__).parent / 'test_config2.json'),
                'someatr2': str(Path(__file__).parent / 'test_config2.json'),
            }
        )
        self.assertTrue(settings_instance.test_json)
        self.assertTrue(settings_instance.someatr)
        self.assertTrue(settings_instance.someatr2)

    def test_settings_creation_with_ini_files(self):
        settings_instance = Settings(
            'settings_test',
            {
                'ini': str(Path(__file__).parent / 'test_ini_config.ini'),
                'ini2': str(Path(__file__).parent / 'test_ini_config.ini'),
                'ini3': str(Path(__file__).parent / 'test_ini_config.ini'),
            }
        )
        self.assertTrue(settings_instance.ini)
        self.assertTrue(settings_instance.ini2)
        self.assertTrue(settings_instance.ini3)

        self.assertEqual(settings_instance.ini['INI']['var'], '2')
        self.assertEqual(settings_instance.ini2['INI']['not number'], 'word')
        self.assertEqual(settings_instance.ini2['INI']['number'], 'some interesting number')

    def test_settings_creation_with_multiple_ini_files(self):
        settings_instance = Settings(
            'settings_test',
            {
                'ini': str(Path(__file__).parent / 'test_ini_config.ini'),
                'cfg': str(Path(__file__).parent / 'test_cfg_file.cfg'),
            }
        )
        self.assertTrue(settings_instance.ini)
        self.assertTrue(settings_instance.cfg)

        self.assertEqual(settings_instance.cfg['CFG']['cfg var'], '1')
        self.assertEqual(settings_instance.cfg['CFG']['not cfg number'], 'cfg')
        self.assertRaises(KeyError, lambda: settings_instance.cfg['CFG']['var'])

        self.assertEqual(settings_instance.ini['INI']['var'], '2')
        self.assertEqual(settings_instance.ini['INI']['not number'], 'word')
        self.assertEqual(settings_instance.ini['INI']['number'], 'some interesting number')

    def test_equal_settings_and_config_file_names(self):
        self.assertRaises(AttributeError, lambda: Settings(
            'settings_test',
            {'another_var': str(Path(__file__).parent / 'test_ini_config.ini')}
        ))

    def test_setup_config_files_after_creating_an_instance_of_the_class(self):
        settings_instance = Settings('settings_test')
        self.assertTrue(settings_instance)

        self.assertRaises(AttributeError, lambda: settings_instance.ini)
        self.assertRaises(AttributeError, lambda: settings_instance.test_json)
        self.assertRaises(AttributeError, lambda: settings_instance.cfg)

        settings_instance.setup_config_files({
            'ini': Path(__file__).parent / 'test_ini_config.ini',
            'cfg': Path(__file__).parent / 'test_cfg_file.cfg',
            'test_json': Path(__file__).parent / 'test_config.json',
        })

        self.assertTrue(settings_instance.ini)
        self.assertTrue(settings_instance.test_json)
        self.assertTrue(settings_instance.cfg)

        self.assertEqual(settings_instance.cfg['CFG']['cfg var'], '1')
        self.assertEqual(settings_instance.cfg['CFG']['not cfg number'], 'cfg')
        self.assertRaises(KeyError, lambda: settings_instance.cfg['CFG']['var'])

        self.assertEqual(settings_instance.ini['INI']['var'], '2')
        self.assertEqual(settings_instance.ini['INI']['not number'], 'word')
        self.assertEqual(settings_instance.ini['INI']['number'], 'some interesting number')
        self.assertTrue(settings_instance.test_json)
        self.assertEqual(settings_instance.test_json['test_var_1'], 1)
        self.assertEqual(settings_instance.test_json['test_var_2'], 'test_var_2 value')
        self.assertEqual(settings_instance.test_json['test_var_3'], 3)
        self.assertEqual(settings_instance.test_json['dict_var']['one'], 1)
        self.assertRaises(KeyError, lambda: settings_instance.test_json['dict_var']['not existed var'])
