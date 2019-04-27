from django.test import LiveServerTestCase
from django.test.client import RequestFactory
from django.urls import reverse
from agrisync.wsgi import application


class WSGITestCase(LiveServerTestCase):
    def setUp(self):
        self.request = RequestFactory()

    def test_wsgi_server(self):
        """test wsgi request generation"""
        request = self.request.get(reverse('main:index'))
        response = application.get_response(request)
        self.assertEqual(response.status_code, 200)
