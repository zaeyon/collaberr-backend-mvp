from django.db import models
from django.conf import settings


class YoutubeCredential(models.Model):
    class Meta:
        db_table = 'youtubecredential'
        verbose_name = 'YoutubeCredential'
        verbose_name_plural = 'YoutubeCredentials'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='account_id',
        primary_key=True,
    )
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()
