from django.conf import global_settings, settings
from django.utils.datastructures import MultiValueDictKeyError
from .json import BaseJson


class SettingField:
    """
    Base settings field
    """
    name = None
    level_of_json = 1

    def __init__(self, setting_name):
        """
        Initialize object with some value
        """
        self.name = setting_name

    def get_value(self):
        """
        Get value of self.name settings
        """
        if self.name.isupper():
            if hasattr(settings, self.name):
                return getattr(settings, self.name)
            elif hasattr(global_settings, self.name):
                return getattr(global_settings, self.name)
            else:
                raise KeyError("Settings %s not found" % self.name)
        else:
            raise IndentationError("Settings %s is not in UPPER case" % self.name)

    def set_value(self, value):
        """
        Set value of self.name settings with value
        """
        if hasattr(settings, self.name):
            return setattr(settings, self.name, value)
        elif hasattr(global_settings, self.name):
            return setattr(global_settings, self.name, value)
        else:
            raise KeyError("Settings %s not found" % self.name)

    def html(self):
        """
        html code for settings
        """
        return "<input type='text' name='" + self.name + "' value='" + str(self.get_value()) + "'>"


class BooleanSettingsField(SettingField):
    """
    Class for boolean settings
    """
    def set_value(self, value):
        if value is None:
            return super(BooleanSettingsField, self).set_value(False)
        elif value == 'on':
            return super(BooleanSettingsField, self).set_value(True)
        else:
            return super(BooleanSettingsField, self).set_value(value)

    def html(self):
        checked = ""
        if self.get_value():
            checked = "checked"
        return "<input type='checkbox' name='" + self.name + "'" + checked + ">"


class Settings(object):
    """
    settings that can be changed by admin panel
    Make sure settings is in upper case
    """

    DEBUG = BooleanSettingsField('DEBUG')
    MAINTENANCE_MODE = BooleanSettingsField('MAINTENANCE_MODE')

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
            getattr(Settings, setting).set_value(data[setting])

    @staticmethod
    def html_settings():
        html = {}
        for setting in dir(Settings):
            if not setting.__contains__('__') and setting.isupper():
                html[setting] = getattr(Settings, setting).html()
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
                    getattr(Settings,setting).set_value(None)
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
