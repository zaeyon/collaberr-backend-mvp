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
