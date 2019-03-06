from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import RedirectView
from .utils import set_settings, set_default, get_settings
from .mixins import SettingsMixin
from django.contrib import messages
from adminsettings.tokens import settings_change_token


SUPERUSER_ERROR = 'Only super user can change settings...'
INVALID_TOKEN = "Invalid Token ..."
TOKEN_NOT_FOUND = "Token not found ..."
SUCCESS_MESSAGE = "Settings changed successfully ..."
RESET_MESSAGE = "Settings reset successfully ..."


class SettingsChangeView(SettingsMixin):
    """
    View for settings change
    """
    def get(self, request, *args, **kwargs):
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        context = self.get_context_data(**kwargs)
        context['site_url'] = site_url
        context['has_permission'] = self.has_permission(request)
        context['hash'] = settings_change_token.make_token(request.user)
        if self.has_permission(request):
            return self.render_to_response(context)
        else:
            messages.error(request, SUPERUSER_ERROR)
            return RedirectView.as_view(pattern_name='admin:index')(request)


class SettingsChangeDoneView(SettingsMixin):
    """
    change settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        if self.has_permission(request):
            try:
                if request.POST['hash'] == settings_change_token.make_token(request.user):
                    set_settings(request.POST)
                    messages.success(request, SUCCESS_MESSAGE)
                else:
                    messages.error(request, INVALID_TOKEN)
            except MultiValueDictKeyError:
                messages.warning(request, TOKEN_NOT_FOUND)
            return RedirectView.as_view(pattern_name='settings:settings_change')(request)
        else:
            messages.error(request, SUPERUSER_ERROR)
            return RedirectView.as_view(pattern_name='admin:index')(request)


class SettingsResetView(SettingsMixin):
    """
    reset settings and redirect to change settings
    """
    def get(self, request, *args, **kwargs):
        if self.has_permission(request):
            try:
                if request.GET['hash'] == settings_change_token.make_token(request.user):
                    set_default()
                    set_settings(get_settings())
                    messages.success(request, RESET_MESSAGE)
                else:
                    messages.error(request, INVALID_TOKEN)
            except MultiValueDictKeyError:
                messages.warning(request, TOKEN_NOT_FOUND)
            return RedirectView.as_view(pattern_name='settings:settings_change')(request)
        else:
            messages.error(request, SUPERUSER_ERROR)
            return RedirectView.as_view(pattern_name='admin:index')(request)
