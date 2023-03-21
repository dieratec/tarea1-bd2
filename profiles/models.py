from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user_id = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birthdate = models.DateField(null=True)
    photo = models.ImageField(upload_to='profile_pics', null=True)
