from django.db import models
from django.conf import settings


class Creator(models.Model):
    class Meta:
        db_table = 'creators'
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='creator',
        db_column='account_id',
    )
    earnings = models.PositiveIntegerField(default=0)
