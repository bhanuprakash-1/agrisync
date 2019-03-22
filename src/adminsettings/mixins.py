from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.admin import AdminSite
from adminsettings.utils import html_settings


class SettingsMixin(TemplateView):
    """
    A separate mixin for handling context and user validation for settings site only
    """
    site_url = AdminSite.site_url
    template_name = 'settings.html'

    @staticmethod
    def has_permission(request):
        """
        check whether user is superuser or not
        """
        return request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        update context data
        """
        context = super(SettingsMixin, self).get_context_data(**kwargs)
        context['site_title'] = settings.SITE_TITLE
        context['site_header'] = settings.SITE_HEADER
        context['title'] = 'Change settings'
        context['fields'] = html_settings()
        return context
