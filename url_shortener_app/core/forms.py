import os
import re

from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import EmailValidator


class RegisterForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=50, required=True,
                                    widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    email = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email')
        mobile_number = cleaned_data.get('mobile_number')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        validate = EmailValidator()
        try:
            validate(email)
        except ValidationError as e:
            self.add_error('email', 'Entered email address is not valid.')
        try:
            if not re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
                            mobile_number):
                raise
        except:
            self.add_error('mobile_number', 'Please write a valid mobile number.')
        if password != confirm_password:
            self.add_error('password', "password and confirmation password do not match")

    def save(self):
        user = User.objects.create_user(
            mobile_number=self.instance.mobile_number,
            email=self.instance.email,
            is_active=True,
            password=self.instance.password
        )
        return user


class LoginForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=50, required=True,
                                    widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['mobile_number', 'password']

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        try:
            if not re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
                            mobile_number):
                raise
        except:
            raise ValidationError('Please write a valid mobile number.', code='invalid')
        exists = User.objects.filter(mobile_number=mobile_number).first()
        if not exists:
            raise ValidationError('User with this mobile number does not exist.', code='invalid')
        return mobile_number

    def clean_password(self):
        password = self.cleaned_data['password']
        user = User.objects.get(mobile_number=self.cleaned_data['mobile_number'])
        if not user.check_password(password):
            raise ValidationError('Password is incorrect.', code='invalid')
        return password

    def clean(self):
        # we override the clean method to change the _validate_unique attribute to bypass validate_unique for mobile_number
        self._validate_unique = False
        return self.cleaned_data


class ShortenUrlForm(forms.Form):
    url = forms.CharField(max_length=2048, required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'URL'}),
                          validators=[URLValidator, ])

    def clean_url(self):
        url = self.cleaned_data['url']
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError as e:
            raise ValidationError('Entered URL does not exist!', code='invalid')
        return url
