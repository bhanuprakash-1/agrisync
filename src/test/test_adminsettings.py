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

    def test_user_is_not_logged_in_case_1(self):
        # settings_change url
        response = self.user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_change'))

    def test_user_is_not_logged_in_case_2(self):
        # settings change done url
        response = self.user.get(reverse('settings:settings_change_done'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_change_done'))

    def test_user_is_not_logged_in_case_3(self):
        # settings reset url
        response = self.user.get(reverse('settings:settings_reset'))
        self.assertRedirects(response, reverse('admin:login') + "?next=" + reverse('settings:settings_reset'))

    def test_user_is_not_super_user_case_1(self):
        # settings change url
        response = self.staff_user.get(reverse('settings:settings_change'))
        self.assertRedirects(response, reverse('admin:index'))

    def test_user_is_not_super_user_case_2(self):
        # settings change done url
        response = self.staff_user.post(reverse('settings:settings_change_done'), follow=True)
        self.assertRedirects(response, reverse('admin:index'))

    def test_user_is_not_super_user_case_3(self):
        # settings reset url
        response = self.staff_user.get(reverse('settings:settings_reset'), follow=True)
        self.assertRedirects(response, reverse('admin:index'))

    def test_user_is_super_user_and_without_token_url_case_1(self):
        # settings change url
        response = self.super_user.get(reverse('settings:settings_change'))
        self.assertEqual(response.status_code, 200)

    def test_user_is_super_user_and_without_token_url_case_2(self):
        # settings change done url with get method
        response = self.super_user.get(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_without_token_url_case_3(self):
        # settings change done url with post method
        response = self.super_user.post(reverse('settings:settings_change_done'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_without_token_url_case_4(self):
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset'), follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, TOKEN_NOT_FOUND)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_wrong_token_case_1(self):
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset') + "?hash=wrong-hash", follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, INVALID_TOKEN)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_wrong_token_case_2(self):
        # settings change done url
        response = self.super_user.post(reverse('settings:settings_change_done'), {'hash': 'wrong_hash'}, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, INVALID_TOKEN)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_correct_token_case_1(self):
        # make hash value
        user = User.objects.get(username='test')
        hash_value = settings_change_token.make_token(user)
        # settings reset url
        response = self.super_user.get(reverse('settings:settings_reset') + "?hash=" + hash_value, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, RESET_MESSAGE)
        self.assertRedirects(response, reverse('settings:settings_change'))

    def test_user_is_super_user_and_with_correct_token_case_2(self):
        # make hash value
        user = User.objects.get(username='test')
        hash_value = settings_change_token.make_token(user)
        # settings change done url
        context = {'hash': hash_value, 'MAINTENANCE_MODE': 'on'}
        response = self.super_user.post(reverse('settings:settings_change_done'), context, follow=True)
        for message in response.context['messages']:
            self.assertEqual(message.message, SUCCESS_MESSAGE)
        self.assertRedirects(response, reverse('settings:settings_change'))


class JsonFileTestCase(TestCase):
    @staticmethod
    def test_settings_file():
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
    def test_base_field_case_1(self):
        # init function
        self.settingsField_1 = SettingField('debug')
        with self.assertRaises(IndentationError):
            self.settingsField_1.get_value()

    def test_base_field_case_2(self):
        # init function
        self.settingsField_2 = SettingField('HELLO')
        with self.assertRaises(KeyError):
            self.settingsField_2.get_value()
        with self.assertRaises(KeyError):
            self.settingsField_2.set_value("hello")

    def test_base_field_case_3(self):
        # init function
        self.settingsField_3 = SettingField('DECIMAL_SEPARATOR')
        self.settingsField_3.html()

    def test_boolean_field(self):
        # boolean field
        self.settingsField_1 = BooleanSettingsField('DEBUG')
