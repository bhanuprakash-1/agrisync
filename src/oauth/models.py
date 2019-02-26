from django.contrib.auth.models import User
from django.db import models
from versatileimagefield.fields import VersatileImageField


# use phone number validators

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10, null=False, blank=False, unique=True, )
    aadhar_id = models.CharField(max_length=12, null=False, blank=False, unique=True,
                                 help_text="Enter your Aadhar 12 digit", default="NA")
    age = models.CharField(max_length=3, help_text="Enter your age")
    # media directory to be set
    img_file = VersatileImageField('Image', upload_to='media/farmers_images/')

    # Also can add type of land , size of land etc.

    def __str__(self):
        return self.user.get_full_name()


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10, null=False, blank=False, unique=True)
    email_id = models.EmailField(max_length=254)
    age = models.CharField(max_length=3, help_text="Enter your age")

    # media directory to be set

    img_file = VersatileImageField('Image', upload_to='media/experts_images/')

    def __str__(self):
        return self.user.get_full_name()
