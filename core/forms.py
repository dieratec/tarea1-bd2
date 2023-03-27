from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", )


class UpdateProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", )
