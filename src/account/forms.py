from django import forms
from django.contrib.auth.forms import UserCreationForm
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

    def clean_account_type(self):
        for key, value in self.ACCOUNT_TYPE:
            if self.data.get('account_type') == key:
                return self.cleaned_data['account_type']
        raise forms.ValidationError("Choose from only available option")


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user_id = self.request.user.id
        return super(FarmerForm, self).save(commit)


class ExpertForm(UserProfileForm):
    skills = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ExpertAccount
        fields = ['profile', 'cover', 'state', 'district', 'skills']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExpertForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user_id = self.request.user.id
        return super(ExpertForm, self).save(commit)
