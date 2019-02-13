from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.conf import settings


class MaintenanceMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not (request.path.startswith('/admin/') or request.path.startswith('/favicon.ico')) and \
                hasattr(settings, 'MAINTENANCE_MODE') and settings.MAINTENANCE_MODE:
            context = {'message': "We are having maintenance please visit again"}
            return render(request, '503.html', context, None, 503)
