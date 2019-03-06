from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from adminsettings.views import TOKEN_NOT_FOUND


class AdminSettingsTestCase(TestCase):
    def setUp(self):
        self.user = Client(enforce_csrf_checks=True)

    def test_user_is_not_logged_in(self):
        # Hit all possible urls without login
        response = self.user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:login')+"?next="+reverse('settings:settings_change'))
        response = self.user.get(reverse('settings:settings_change_done'))
        self.assertRedirects(response, reverse('admin:login')+"?next="+reverse('settings:settings_change_done'))
        response = self.user.get(reverse('settings:settings_reset'))
        self.assertRedirects(response, reverse('admin:login')+"?next="+reverse('settings:settings_reset'))

    def test_user_is_not_super_user(self):
        # login with staff account
        user = self.user
        user.force_login(User.objects.get_or_create(username='test', is_staff=True)[0])
        # Hit urls with only staff account
        response = user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:index'))
        response = user.get('/admin/settings/change_done/', follow=True)
        self.assertRedirects(response, reverse('admin:index'))
        response = user.get('/admin/settings/reset/', follow=True)
        self.assertRedirects(response, reverse('admin:index'))

    def test_user_is_super_user(self):
        # Login with superuser account
        user = self.user
        user.force_login(User.objects.get_or_create(username='test', is_staff=True, is_superuser=True)[0])
        # hit change urls
        response = user.get(reverse('settings:settings_change'))
        self.assertEqual(response.status_code, 200)
        # Hit change_done and reset urls without tokens
        response = user.get(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        response = user.get(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
