from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse


class MaintenanceMiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_comman_maintenance_mode(self):
        # maintenance mode app variable exist and maintenance mode variable exist
        setattr(settings, 'MAINTENANCE_MODE', True)
        setattr(settings, 'MAINTENANCE_MODE_APP', ('main',))
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 503)
        setattr(settings, 'MAINTENANCE_MODE', False)
        # maintenance mode app variable
        setattr(settings, 'MAIN_APP_MAINTENANCE', True)
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 503)
        setattr(settings, 'MAIN_APP_MAINTENANCE', False)
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
