from .fields import BooleanSettingsField
from django.utils.datastructures import MultiValueDictKeyError
from .json import BaseJson


class Settings(object):
    """
    settings that can be changed by admin panel
    Make sure settings is in upper case
    """

    DEBUG = BooleanSettingsField('DEBUG', verbous_name='Debug')
    MAINTENANCE_MODE = BooleanSettingsField('MAINTENANCE_MODE',  verbous_name='Maintenance Mode')
    MAIN_APP_MAINTENANCE = BooleanSettingsField('MAIN_APP_MAINTENANCE',  verbous_name='Main app maintenance')
    OAUTH_APP_MAINTENANCE = BooleanSettingsField('OAUTH_APP_MAINTENANCE', verbous_name='Oauth app maintenance')
    FORUM_APP_MAINTENANCE = BooleanSettingsField('FORUM_APP_MAINTENANCE', verbous_name='Forum app maintenance')

    @staticmethod
    def __init__():
        """
        call all necessary function at initial
        """
        Settings.save_default()
        Settings.load_settings()

    @staticmethod
    def save_default():
        """
        save default settings to json file
        """
        data = {}
        for setting in dir(Settings):
            if not setting.__contains__('__') and setting.isupper():
                data[setting] = getattr(Settings, setting).get_value()
        return BaseJson.set_default(data)

    @staticmethod
    def load_settings():
        """
        get all settings of this class
        """
        data = BaseJson.get_settings()
        for setting in data:
            try:
                getattr(Settings, setting).set_value(data[setting])
            except AttributeError:
                pass

    @staticmethod
    def html_settings():
        html = {}
        for setting in dir(Settings):
            if not setting.__contains__('__') and setting.isupper():
                html[getattr(Settings, setting).verbous_name] = getattr(Settings, setting).html()
        return html

    @staticmethod
    def save_settings():
        """
        save all settings in file
        """
        return BaseJson.set_settings(Settings.get_settings())

    @staticmethod
    def get_settings():
        """
        get all settings
        """
        data = {}
        for setting in dir(Settings):
            if not setting.__contains__('__') and setting.isupper():
                data[setting] = getattr(Settings, setting).get_value()
        return data

    @staticmethod
    def set_settings(data):
        """
        get value form user and set into variable
        """
        for setting in dir(Settings):
            if not setting.__contains__('__') and setting.isupper():
                try:
                    getattr(Settings, setting).set_value(data[setting])
                except MultiValueDictKeyError:
                    getattr(Settings, setting).set_value(None)
        Settings.save_settings()

    @staticmethod
    def get_default():
        """
        get default settings
        """
        return BaseJson.get_default()

    @staticmethod
    def set_default():
        """
        set default settings to settings object
        """
        data = BaseJson.get_default()
        for setting in data:
            getattr(Settings, setting).set_value(data[setting])


allsettings = Settings()
