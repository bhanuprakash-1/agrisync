from django.contrib.auth.models import User
from django.test import TestCase, Client


class AdminSettingsTestCase(TestCase):
    def setUp(self):
        self.user = Client(enforce_csrf_checks=True)

    def test_user_is_not_logged_in(self):
        response = self.user.get('/admin/settings/change/')
        self.assertRedirects(response, '/admin/login/?next=/admin/settings/change/')

    def test_user_is_not_super_user(self):
        user = self.user
        user.force_login(User.objects.get_or_create(username='test', is_staff=True)[0])
        response = user.get('/admin/settings/change/')
        self.assertRedirects(response, '/admin/')

    def test_user_is_super_user(self):
        user = self.user
        user.force_login(User.objects.get_or_create(username='test', is_staff=True, is_superuser=True)[0])
        response = user.get('/admin/settings/change/')
        self.assertEqual(response.status_code, 200)
