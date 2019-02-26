from .mixins import SettingsMixin, RedirectMixin
from .settings import allsettings
from django.contrib import messages


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
        messages.success(request, "Settings changed successfully ...")
        return RedirectMixin.as_view(redirect_url='settings:settings_change')(request)


class SettingsResetView(SettingsMixin):
    """
    reset settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        allsettings.set_default()
        allsettings.set_settings(allsettings.get_settings())
        messages.success(request, "Settings reset successfully ...")
        return RedirectMixin.as_view(redirect_url='settings:settings_change')(request)
