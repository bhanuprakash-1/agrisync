from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from account.models import FarmerAccount, ExpertAccount


class AccountModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.farmer = FarmerAccount.objects.create(user=cls.user)
        cls.expert = ExpertAccount.objects.create(user=cls.user)

    def test_userprofile_str_method(self):
        """str method of userprofile"""
        self.assertEqual(self.farmer.__str__(), "-India")

    def test_userprofile_get_absolute_url_method(self):
        """get absolute url of userprofile"""
        self.assertEqual(self.farmer.get_absolute_url(), reverse('account:profile'))

    def test_farmer_major_crop_list_property_case_1(self):
        """no property included"""
        self.assertEqual(self.farmer.major_crop_list, '')

    def test_farmer_major_crop_list_property_case_2(self):
        """property included"""
        self.farmer.major_crop = "abc"
        self.farmer.save()
        self.assertEqual(self.farmer.major_crop_list, ['abc'])
        self.farmer.major_crop = ''
        self.farmer.save()

    def test_expert_skills_list_property_case_1(self):
        """no skills included"""
        self.assertEqual(self.expert.skills_list, '')

    def test_expert_skills_list_property_case_2(self):
        """skills included"""
        self.expert.skills = "abc"
        self.expert.save()
        self.assertEqual(self.expert.skills_list, ['abc'])
        self.expert.skills = ''
        self.expert.save()
