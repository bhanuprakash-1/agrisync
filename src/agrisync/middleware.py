from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.conf import settings
from django.urls import resolve


class MaintenanceMiddleware(MiddlewareMixin):
    """
    Middleware for checking maintenance for individual app or all app
    """
    maintenance_mode = None

    def process_request(self, request):
        """
        First check for general MAINTENANCE_MODE then check individual app maintenance
        """
        if hasattr(settings, 'MAINTENANCE_MODE_APP') and \
                settings.MAINTENANCE_MODE_APP.__contains__(resolve(request.path).app_name) and \
                hasattr(settings, 'MAINTENANCE_MODE') and settings.MAINTENANCE_MODE:
            context = {'message': 'We are having maintenance please visit again'}
            return render(request, '503.html', context, None, 503)

        try:
            self.maintenance_mode = resolve(request.path).kwargs['MAINTENANCE']
        except KeyError:
            self.maintenance_mode = resolve(request.path).app_name.upper() + "_APP_MAINTENANCE"

        if hasattr(settings, self.maintenance_mode) and getattr(settings, self.maintenance_mode):
            context = {'message': '%s service is not available' % resolve(request.path).app_name.capitalize()}
            return render(request, '503.html', context, None, 503)
