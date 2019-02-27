from django.conf import settings, global_settings


class SettingField:
    """
    Base settings field
    """
    name = None
    verbous_name = None
    level_of_json = 1

    def __init__(self, setting_name, **options):
        """
        Initialize object with some value
        """
        self.name = setting_name
        if 'verbous_name' in options:
            self.verbous_name = options['verbous_name']
        else:
            self.verbous_name = setting_name

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
        return "<input type='checkbox' name='" + self.name + "' " + checked + ">"
