from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'})
        }


class UpdateProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "photo", "birthdate")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'photo': forms.FileInput(attrs={'class': 'file-input'}),
            'birthdate': forms.DateInput(attrs={'class': 'input', 'type': 'date'}, format="%Y-%m-%d"),
        }
