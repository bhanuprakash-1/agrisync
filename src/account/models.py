from django.contrib.auth.models import User, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from versatileimagefield.fields import VersatileImageField


class UserProfileManager(UserManager):
    pass


class UserProfile(models.Model):
    # Validators
    CONTACT = RegexValidator(r'^[0-9]{10}$', message="Invalid mobile number")
    # Database Field
    # One to one field to django's in built User model to handle authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, validators=[CONTACT], blank=True,
                             help_text="Enter your 10 digit mobile number")
    address = models.TextField(blank=True)
    country = CountryField(default='IN')
    email_confirmed = models.BooleanField(default=False)
    phone_confirmed = models.BooleanField(default=False)

    # future field
    # dob = models.DateField(blank=True)
    # aadhar = models.BigIntegerField(blank=True)
    # verified_user = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.get_full_name() + "-" + self.country.name

    @staticmethod
    def get_absolute_url():
        return reverse('account:profile')


class FarmerAccount(UserProfile):
    # Database field
    profile = VersatileImageField(upload_to='farmer/profile', blank=True, null=True)
    cover = VersatileImageField(upload_to='farmer/cover', blank=True, null=True)
    land_area = models.FloatField(max_length=7, blank=True, null=True)
    # Needs to be change
    state = models.CharField(max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    major_crop = models.TextField(blank=True, help_text='Enter major crops separated by comma', null=True)

    @property
    def major_crop_list(self):
        if self.major_crop == '' or not self.major_crop:
            return ''
        return sorted(self.major_crop.split(','))


class ExpertAccount(UserProfile):
    # Database filed
    profile = VersatileImageField(upload_to='expert/profile', blank=True, null=True)
    cover = VersatileImageField(upload_to='expert/cover', blank=True, null=True)
    # Need to be change
    state = models.CharField(max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    skills = models.TextField(blank=True, help_text='Enter skills separated by comma', null=True)

    @property
    def skills_list(self):
        if self.skills == '' or not self.skills:
            return ''
        return sorted(self.skills.split(','))
