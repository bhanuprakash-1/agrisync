from .mixins import SettingsMixin
from .settings import allsettings


class SettingsChangeView(SettingsMixin):
    """
    View for settings change
    """
    pass


class SettingsChangeDoneView(SettingsMixin):
    """
    change settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        allsettings.set_settings(request.POST)
        return super(SettingsChangeDoneView, self).get(request, *args, **kwargs)


class SettingsResetView(SettingsMixin):
    """
    reset settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        allsettings.set_default()
        allsettings.set_settings(allsettings.get_settings())
        return super(SettingsResetView, self).get(request, *args, **kwargs)
