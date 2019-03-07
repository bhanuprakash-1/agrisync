import os
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from adminsettings.views import TOKEN_NOT_FOUND, INVALID_TOKEN, SUCCESS_MESSAGE, RESET_MESSAGE
from adminsettings.tokens import settings_change_token
from adminsettings.fields import SettingField, BooleanSettingsField
from adminsettings.json import BaseJson
from django.conf import settings


class AdminSettingsTestCase(TestCase):
    def setUp(self):
        # Normal user
        self.user = Client()
        # Staff user
        self.staff_user = Client()
        self.staff_user.force_login(User.objects.get_or_create(username='test_staff', is_staff=True)[0])
        # Super User
        self.super_user = Client()
        self.super_user.force_login(User.objects.get_or_create(username='test', is_staff=True, is_superuser=True)[0])

    def test_user_is_not_logged_in(self):
        # Hit all possible urls without login
        # settings_change url
        response = self.user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_change'))
        # settings change done url
        response = self.user.get(reverse('settings:settings_change_done'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_change_done'))
        # settings reset url
        response = self.user.get(reverse('settings:settings_reset'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_reset'))

    def test_user_is_not_super_user(self):
        # Hit urls with only staff account
        # settings change url
        response = self.staff_user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:index'))
        # settings change done url
        response = self.staff_user.post('/admin/settings/change_done/', follow=True)
        self.assertRedirects(response, reverse('admin:index'))
        # settings reset url
        response = self.staff_user.get('/admin/settings/reset/', follow=True)
        self.assertRedirects(response, reverse('admin:index'))

    def test_user_is_super_user_and_without_token_url(self):
        # hit url with superuser account and without token
        # settings change url
        response = self.super_user.get(reverse('settings:settings_change'))
        self.assertEqual(response.status_code, 200)
        # settings change done url with get method
        response = self.super_user.get(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))
        # settings change done url with post method
        response = self.super_user.post(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_wrong_token(self):
        # hit url with superuser and wrong hash value
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset') + "?hash=wrong-hash", follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, INVALID_TOKEN)
        self.assertRedirects(response, reverse('settings:settings_change'))
        # settings change done url
        response = self.super_user.post(reverse('settings:settings_change_done'), {'hash': 'wrong_hash'}, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, INVALID_TOKEN)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_correct_token(self):
        # hit url with super user and correct hash value
        # make hash value
        user = User.objects.get(username='test')
        hash_value = settings_change_token.make_token(user)
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset') + "?hash=" + hash_value, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, RESET_MESSAGE)
        self.assertRedirects(response, reverse('settings:settings_change'))
        # settings change done url
        context = {'hash': hash_value, 'DEBUG': 'on'}
        response = self.super_user.post(reverse('settings:settings_change_done'), context, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, SUCCESS_MESSAGE)
        self.assertRedirects(response, reverse('settings:settings_change'))


class JsonFileTestCase(TestCase):
    def test_settings_file(self):
        os.system('rm ../default_settings.json')
        os.system('rm ../settings.json')
        delattr(settings, "JSON_SETTINGS_FILE")
        delattr(settings, "DEFAULT_JSON_SETTINGS_FILE")
        data = BaseJson.get_settings()
        data['DEBUG'] = True
        data['test'] = True
        BaseJson.set_settings(data)
        data = BaseJson.get_default()
        BaseJson.set_default(data)


class SettingsFieldTestCase(TestCase):
    def test_base_field(self):
        # init function
        self.settingsField_1 = SettingField('debug')
        self.settingsField_2 = SettingField('HELLO')
        self.settingsField_3 = SettingField('DECIMAL_SEPARATOR')
        with self.assertRaises(IndentationError):
            self.settingsField_1.get_value()
        with self.assertRaises(KeyError):
            self.settingsField_2.get_value()
        with self.assertRaises(KeyError):
            self.settingsField_2.set_value("hello")
        self.settingsField_3.html()

    def test_boolean_field(self):
        # boolean field
        self.settingsField_1 = BooleanSettingsField('DEBUG')
