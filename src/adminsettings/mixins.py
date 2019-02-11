from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.contrib.admin import AdminSite
from .settings import allsettings


class RedirectMixin(RedirectView):
    """
    If user is not authorised then redirect home page
    """
    redirect_url = 'admin:index'
    urlconf = None
    args = None
    kwargs = None
    current_app = None

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.redirect_url, self.urlconf, self.args, self.kwargs, self.current_app)


class SettingsMixin(TemplateView, RedirectMixin):
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
        context['fields'] = allsettings.html_settings()
        return context

    def get(self, request, *args, **kwargs):
        """
        Update get method for request based context
        """
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        context = self.get_context_data(**kwargs)
        context['site_url'] = site_url
        context['has_permission'] = self.has_permission(request)
        if self.has_permission(request):
            return self.render_to_response(context)
        else:
            return RedirectMixin.as_view()(request)
