from django.utils.datastructures import MultiValueDictKeyError
from .utils import set_settings, set_default, get_settings
from .mixins import SettingsMixin, RedirectMixin
from django.contrib import messages
from adminsettings.tokens import settings_change_token


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
        try:
            if request.POST['hash'] == settings_change_token.make_token(request.user):
                set_settings(request.POST)
                messages.success(request, "Settings changed successfully ...")
            else:
                messages.error(request, "Invalid Token ...")
        except MultiValueDictKeyError:
            messages.warning(request, "Token not found ...")
        return RedirectMixin.as_view(redirect_url='settings:settings_change')(request)


class SettingsResetView(SettingsMixin):
    """
    reset settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        try:
            if request.GET['hash'] == settings_change_token.make_token(request.user):
                set_default()
                set_settings(get_settings())
                messages.success(request, "Settings reset successfully ...")
            else:
                messages.error(request, "Invalid Token ...")
        except MultiValueDictKeyError:
            messages.warning(request, "Token not found ...")
        return RedirectMixin.as_view(redirect_url='settings:settings_change')(request)
