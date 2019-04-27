from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from account.models import FarmerAccount


class AccountURLTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='test', password='hirenchalodiya')
        cls.farmer = FarmerAccount.objects.create(user=cls.user)
        cls.staff = User.objects.create_user(username='staff', password='hirenchalodiya', is_staff=True)
        cls.random = User.objects.create_user(username='random', password='hirenchalodiya')

    def test_profile_url_case_1(self):
        """user is not logged in"""
        response = self.client.get(reverse('account:profile'), follow=True)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('account:profile'))

    def test_profile_url_case_2(self):
        """user is logged in"""
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('account:profile'), follow=True)
        self.assertTemplateUsed(response, 'account/profile.html')
        self.client.logout()

    def test_register_url_case_1(self):
        """chosen type is FA"""
        data = {'username': 'test1', 'account_type': 'FA', 'password1': 'hirenchalodiya', 'password2': 'hirenchalodiya'}
        res = self.client.post(reverse('account:register'), data, follow=True)
        self.assertRedirects(res, reverse('account:farmer-register'))

    def test_register_url_case_2(self):
        """chosen type is EA"""
        data = {'username': 'test1', 'account_type': 'EA', 'password1': 'hirenchalodiya', 'password2': 'hirenchalodiya'}
        res = self.client.post(reverse('account:register'), data, follow=True)
        self.assertRedirects(res, reverse('account:expert-register'))

    def test_register_url_case_3(self):
        """chosen type is invalid"""
        data = {'username': 'test1', 'account_type': 'AB', 'password1': 'hirenchalodiya', 'password2': 'hirenchalodiya'}
        res = self.client.post(reverse('account:register'), data, follow=True)
        self.assertTemplateUsed(res, 'account/register.html')

    def test_register_farmer_url(self):
        """without logged in user test"""
        data = {'major_crop': 'test_crop, ab', 'phone': '1234567890', 'address': 'a'}
        res = self.client.post(reverse('account:farmer-register'), data, follow=True)
        self.assertRedirects(res, reverse('login') + "?next=" + reverse('account:farmer-register'))

    def test_register_expert_url(self):
        """with logged in user"""
        self.client.force_login(self.user)
        data = {'skills': 'test_crop, ab', 'phone': '1234567890', 'address': 'a', 'country': 'IN'}
        res = self.client.post(reverse('account:expert-register'), data, follow=True)
        self.assertRedirects(res, reverse('account:profile'))

    def test_login_url_case_1(self):
        """user is random"""
        data = {'username': 'random', 'password': 'hirenchalodiya'}
        res = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(res, reverse('account:farmer-register'))
        self.client.logout()

    def test_login_url_case_2(self):
        """user is staff"""
        data = {'username': 'staff', 'password': 'hirenchalodiya'}
        res = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(res, reverse('admin:index'))
        self.client.logout()

    def test_login_url_case_3(self):
        """user is farmer or expert"""
        data = {'username': 'test', 'password': 'hirenchalodiya'}
        res = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(res, reverse('forum:index'))
        self.client.logout()
