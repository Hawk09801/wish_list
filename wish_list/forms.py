from django.contrib.auth import authenticate
from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# formularz do logowania

def my_validator(value):
    if value.find('@') == -1:
        raise ValidationError("to nie jest email")


class LoginUserForm(forms.Form):
    email = forms.EmailField(validators=[my_validator], label="Podaj adres e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Wprowadź hasło")

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Podany login i/lub hasło jest niepoprawne")
        return self.cleaned_data

'''
    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            self.add_error("email", "Konto nie istnieje")
            return cleaned_data

        password = cleaned_data.get('password')
        user = User.objects.get(email=email)

        if password != user.password:
            self.add_error("password", "Niepoprawne hasło")

        return cleaned_data
'''

# formularz tworzenia nowego użytkownika
class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=64, label="Podaj imię")
    last_name = forms.CharField(max_length=64, label="Podaj nazwisko")
    email = forms.EmailField(validators=[my_validator], label="Podaj adres e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Wprowadź hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Potwierdź hasło")

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email zajęty!")

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error("password", "Hasła muszą być takie same!")

        return cleaned_data

# dodawanie prezentów do listy
class AddGiftToListForm(ModelForm):
    class Meta:
        model = Gifts
        exclude = ['wish_list', 'person']



# edycja prezentu:
class EditGiftForm(ModelForm):
    class Meta:
        model = Gifts
        exclude = ['person']
        widgets = {'wish_list': forms.HiddenInput, 'pk': forms.HiddenInput}


class SearchForm(forms.Form):
    last_name = forms.CharField(max_length=64, label='Wyszukaj osobę po nazwisku')


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {'email': forms.TextInput(attrs={'readonly':'readonly'})}
        labels = {
            'first_name': ('Imię:'),
            'last_name': ('Nazwisko:'),
            'email': ('Adres e-mail:'),
        }
        help_texts = {
            'email': ('Nie można edytować adresu e-mail'),
        }


class EditPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_date = super().clean()

        field1 = cleaned_date.get('new_password')
        field2 = cleaned_date.get('repeat_password')
        if field1 != field2:
            raise ValidationError("Wpisane hasła muszą być takie same")

        return cleaned_date


class AddFundraiserForm(ModelForm):
    class Meta:
        model = Fundraiser
        exclude = ['user']


class AddDonorForm(ModelForm):
    class Meta:
        model = Donors
        fields = ['amount']