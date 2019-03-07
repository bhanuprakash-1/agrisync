from django.test import TestCase
from django.contrib.auth.models import User
from oauth.models import Farmer


class OauthURLTestCase(TestCase):
    pass


class FarmerModelTestCase(TestCase):
    def setUp(self):
        User.objects.get_or_create(username='farmer_1')
        self.farmer = Farmer.objects.get_or_create(user=User.objects.get(username='farmer_1'))

    def test_basic(self):
        self.farmer.__str__()
