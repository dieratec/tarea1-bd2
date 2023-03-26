from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)


class Download(models.Model):
    download_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    download_at = models.DateTimeField(auto_now_add=True)
    dataset_download = models.JSONField()
    dataset_id = models.BigIntegerField()
