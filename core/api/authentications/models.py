from django.db import models
from django.conf import settings


class JWTToken(models.Model):
    class Meta:
        db_table = 'jwttokens'
        verbose_name = 'JWTToken'
        verbose_name_plural = 'JWTTokens'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='account_id',
        primary_key=True,
    )
    refresh_token = models.TextField()
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_expires_at = models.DateTimeField()
    access_expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)


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
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scope = models.TextField()
