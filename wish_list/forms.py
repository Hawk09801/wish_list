from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# formularz do logowania

class LoginUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput}