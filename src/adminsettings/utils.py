from .json import BaseJson
from django.utils.datastructures import MultiValueDictKeyError
from .settings import Settings


def save_default():
    """
    save default settings to json file
    """
    data = {}
    for setting in dir(Settings):
        if not setting.__contains__('__') and setting.isupper():
            data[setting] = getattr(Settings, setting).get_value()
    return BaseJson.set_default(data)


def load_settings():
    """
    get all settings of this class
    """
    data = BaseJson.get_settings()
    for setting in data:
        try:  # pragma: no cover
            getattr(Settings, setting).set_value(data[setting])
        except AttributeError:  # pragma: no cover
            pass


def html_settings():
    html = {}
    for setting in dir(Settings):
        if not setting.__contains__('__') and setting.isupper():
            html[getattr(Settings, setting).verbous_name] = getattr(Settings, setting).html()
    return html


def save_settings():
    """
    save all settings in file
    """
    return BaseJson.set_settings(get_settings())


def get_settings():
    """
    get all settings
    """
    data = {}
    for setting in dir(Settings):
        if not setting.__contains__('__') and setting.isupper():
            data[setting] = getattr(Settings, setting).get_value()
    return data


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
    save_settings()


def get_default():
    """
    get default settings
    """
    return BaseJson.get_default()


def set_default():
    """
    set default settings to settings object
    """
    data = BaseJson.get_default()
    for setting in data:
        getattr(Settings, setting).set_value(data[setting])
