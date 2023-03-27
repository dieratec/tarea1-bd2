from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm, UpdateProfileForm
from .models import User


class ManageUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = UpdateProfileForm
    model = User
    list_display = ["username",]


admin.site.register(User, UserAdmin)
