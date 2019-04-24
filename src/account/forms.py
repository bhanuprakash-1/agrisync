from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from account.models import FarmerAccount, ExpertAccount


class UserForm(UserCreationForm):
    ACCOUNT_TYPE = (
        ('FA', 'Farmer'),
        ('EA', 'Expert')
    )
    account_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'text'}), choices=ACCOUNT_TYPE)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text email', 'type': 'password', 'name': 'password', 'placeholder': 'Password'}), strip=False,
                                label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text w3lpass', 'type': 'password', 'name': 'password', 'placeholder': 'Confirm Password'}),
                                strip=False, label='')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'text', 'type': 'text', 'name': 'Username', 'placeholder': 'Username'}),
        label='')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class UserProfileForm(forms.ModelForm):
    # Validators
    CONTACT = RegexValidator(r'^[0-9]{10}$', message="Invalid mobile number")
    # fields
    phone = forms.CharField(max_length=10, validators=[CONTACT])
    address = forms.CharField(widget=forms.Textarea)
    country = CountryField(default='IN').formfield()

    class Meta:
        fields = ['phone', 'address', 'country']
        abstract = True


class FarmerForm(UserProfileForm):
    major_crop = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = FarmerAccount
        fields = ['profile', 'cover', 'land_area', 'state', 'district', 'major_crop']


class ExpertForm(UserProfileForm):
    skills = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ExpertAccount
        fields = ['profile', 'cover', 'state', 'district', 'skills']
