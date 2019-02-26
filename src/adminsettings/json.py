from django.conf import settings
import json


class BaseJson:
    @staticmethod
    def get_settings():
        """
        get all changed settings
        """
        try:
            file_name = settings.JSON_SETTINGS_MODULE
        except AttributeError:
            file_name = 'settings.json'
        data = {}
        try:
            with open(file_name, 'r') as infile:
                data = json.load(infile)
            return data
        except FileNotFoundError:
            with open(file_name, 'w') as outfile:
                outfile.write('{}')
            return data

    @staticmethod
    def set_settings(data):
        """
        set all settings from data object to json file
        """
        try:
            file_name = getattr(settings, 'JSON_SETTINGS_FILE')
        except AttributeError:
            file_name = 'settings.json'
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def get_default():
        """
        get all default settings and save in data object
        """
        try:
            file_name = getattr(settings, 'DEFAULT_JSON_SETTINGS_FILE')
        except AttributeError:
            file_name = 'default_settings.json'

        try:
            with open(file_name, 'r') as infile:
                data = json.load(infile)
            return data
        except FileNotFoundError:
            from .utils import save_default, get_default
            save_default()
            return get_default()

    @staticmethod
    def set_default(data):
        """
        save default setting to json file
        """
        try:
            file_name = getattr(settings, 'DEFAULT_JSON_SETTINGS_FILE')
        except AttributeError:
            file_name = 'default_settings.json'
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
