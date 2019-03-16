from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=255,default="")
    phone = models.CharField(max_length=15,blank=True, help_text="Enter mobile number")
    farmer = models.BooleanField(default=True)
    expert = models.BooleanField(default=False)
    dob = models.DateField()
    # aadhar_validator = RegexValidator(r'^[0-9]{12}$', message='Not a valid Aadhar  number!')
    aadhar = models.BigIntegerField()
    img_file = VersatileImageField('Image', upload_to='media/farmers_images/')
    land_area = models.FloatField(max_length=4, blank=False, help_text="Land In Acres")
    registration_date = models.DateTimeField(auto_now_add=True)

    """  Add location of land ....  """

    def __str__(self):
        return self.full_name


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=15,blank=True, help_text="Enter mobile number")
    farmer = models.BooleanField(default=False)
    expert = models.BooleanField(default=True)
    dob= models.DateField()
    registration_date = models.DateTimeField(auto_now_add=True)
    email_id = models.EmailField(max_length=254, blank=False, help_text="Enter you email id")
    skills = models.TextField()

    """ How to save image file with name of user?    """

    img_file = VersatileImageField('Image', upload_to='media/experts_images/')

    def __str__(self):
        return self.full_name


"""
class AbstractUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
     phone number validators 
    phone_validator = RegexValidator(r'^\+?1?\d{9,15}$', message='Invalid mobile number.')
    phone_no = models.IntegerField(phone_validator, help_text="Enter correct mobile number")
     to differentiate whether expert or farmer
    farmer = models.BooleanField(default=False)
    expert = models.BooleanField(default=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200), MinValueValidator(10)],
                                           help_text="Enter correct age")
    date = models.DateField(default=True, auto_now_add=True)

    class Meta:
        abstract = True


class Farmer(AbstractUser):
    aadhar_validator = RegexValidator(r'^[0-9]{12}$', message='Not a valid Aadhar  number!')
    aadhar = models.BigIntegerField(validators=aadhar_validator)
    # media directory to be set
    img_file = VersatileImageField('Image', upload_to='media/farmers_images/')
    land_area = models.FloatField(max_length=4, blank=False, help_text="In hectares")

    def __str__(self):
        return self.user

    def is_farmer(self):
        return self.farmer

    def is_expert(self):
        return self.expert


class Expert(AbstractUser):
    email_id = models.EmailField(max_length=254, blank=False, help_text="Enter you email id")
    skills = models.TextField()
    img_file = VersatileImageField('Image', upload_to='media/experts_images/')

    def __str__(self):
        return self.user

    def is_farmer(self):
        return self.farmer

    def is_expert(self):
        return self.expert

"""
