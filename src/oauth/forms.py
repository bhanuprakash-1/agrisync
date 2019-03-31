from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import Farmer
from django.contrib.auth import authenticate

class FarmerRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(label='Password confirmation',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text='Enter the same password as before, for verification.',
                                )
    username = forms.CharField(max_length=30, help_text="Enter username you like", label='Username')
    full_name = forms.CharField(max_length=50, help_text="Enter your full name")
    phone = forms.IntegerField(help_text="Enter your phone number")
    dob = forms.DateField(help_text="Enter your DOB ex: 2000-01-25", required=False)
    aadhar = forms.IntegerField(help_text="Enter your Aadhar Number", required=False)
    land_area = forms.FloatField(help_text="Enter your Land area in acres")
    income = forms.ChoiceField(help_text="Enter your annual Income in Lacs",choices=Farmer.Income_choices)
    major_crop = forms.CharField(max_length=220, help_text="Enter your major crop", required=False)
    img_file = forms.ImageField(required=False)
    state = forms.CharField(max_length=35, required=False)
    district = forms.CharField(max_length=35, required=False)

    """  Can add validation errors for fields  """

    def clean_aadhar(self):
        # to check if aadhar number is valid or not
        value = self.cleaned_data['aadhar']
        if len(str(value)) != 12:
            raise forms.ValidationError(""" Please Enter valid aadhar no""")
        return value

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ExpertRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(label='Password confirmation',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text='Enter the same password as before, for verification.',
                                )
    username = forms.CharField(max_length=30, help_text="Enter username you like", label='Username')
    full_name = forms.CharField(max_length=50, help_text="Enter your full name")
    email_id = forms.EmailField(required=False, help_text="Enter email id")
    phone = forms.IntegerField(help_text="Enter your phone number", required=True)
    dob = forms.DateField(help_text="Enter your DOB ex: 2000-01-25")
    skills = forms.CharField(max_length=300, required=True, help_text="Enter your skills")
    postal_add = forms.CharField(max_length=200, help_text="Enter your postal address", required=True)
    img_file = forms.ImageField(required=False, help_text="Input your image")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, help_text="Enter your registered username", label='Username')
    password = forms.CharField(label='Password',
                               strip=False,
                               widget=forms.PasswordInput(),
                               help_text=password_validation.password_validators_help_text_html(),
                               )

    def clean(self):
        super(LoginForm,self).clean()
        username = self.cleaned_data.get('username','')
        password = self.cleaned_data.get('password', '')

        user = authenticate(username=username, password=password)

        if user is  None:
            raise forms.ValidationError("Username or password does not exist")

    def get_user(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username, password=password)
        return user


# This form is  not used anywhere required

class Password_ChangeForm(forms.Form):
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Password',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    new_password2 = forms.CharField(label='Password confirmation',
                                strip=False,
                                widget=forms.PasswordInput(),
                                help_text='Enter the same password as before, for verification.',
                                )


    def clean_old_password(self):

        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(""" Enter correct old password """)
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(""" New Passwords didn't match """)
        return password2
