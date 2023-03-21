from django.db import models
from django.contrib.auth import get_user_model


class Download(models.Model):
    downloaded_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)
    dataset_download = models.JSONField()
    dataset_id = models.BigIntegerField()
