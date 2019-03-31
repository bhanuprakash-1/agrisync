from django.contrib.admin import AdminSite
from django.urls import path
from django.views.decorators.cache import never_cache


class AdminSettings(AdminSite):
    """
    Additional urls form change setting in  django
    """
    settings_title = 'Change settings'

    def get_urls(self):
        """
        Override get_urls function
        """
        def wrap(view, cacheable=False):
            from functools import update_wrapper

            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        urlpatterns = [
            path('change/', wrap(self.settings_change), name='settings_change'),
            path('change_done/', wrap(self.settings_change_done), name='settings_change_done'),
            path('reset/', wrap(self.settings_reset), name='settings_reset'),
        ]
        return urlpatterns

    @property
    def urls(self):
        """
        Override urls function
        """
        return self.get_urls(), 'settings', self.name

    @never_cache
    def settings_change(self, request):
        from .views import SettingsChangeView
        """
        Display the main settings page, which lists all settings which can be changed fro admin panel
        """
        return SettingsChangeView.as_view()(request)

    @never_cache
    def settings_change_done(self, request):
        from .views import SettingsChangeDoneView
        """
        Change settings and display settings_page
        """
        return SettingsChangeDoneView.as_view()(request)

    @never_cache
    def settings_reset(self, request):
        from .views import SettingsResetView
        """
        Reset Settings and display same page
        """
        return SettingsResetView.as_view()(request)


adminsettings = AdminSettings(name='settings')
