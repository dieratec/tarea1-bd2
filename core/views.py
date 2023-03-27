from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegistrationForm


class SignUpView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
