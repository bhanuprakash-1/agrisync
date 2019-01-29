from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Farmer(models.Model):
    """
    Farmer models details and different method of Farmer model
    """

    """ Validators """
    contact = RegexValidator(r'^[0-9]{6,10}$')

    """ """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_1 = models.CharField(max_length=10, validators=(contact, ), blank=True)
    phone_2 = models.CharField(max_length=10, validators=(contact, ), blank=True)

    def __str__(self):
        return self.user.username
