from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import password_validation

from .models import User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label="Contraseña:",
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label="Confirmar contraseña:",
        help_text="Para verificar, introduzca la misma contraseña anterior."
    )

    class Meta:
        model = User
        fields = ("username", )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
        }


class UpdateProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "photo", "birthdate", "email")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'photo': forms.FileInput(attrs={'class': 'file-input'}),
            'birthdate': forms.DateInput(attrs={'class': 'input', 'type': 'date'}, format="%Y-%m-%d"),
            "email": forms.TextInput(attrs={'class': 'input'}),
        }
