from django.db import models
from django.conf import settings


class Business(models.Model):
    class Meta:
        db_table = 'businesses'
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business',
        db_column='account_id',
    )
    id = models.AutoField(primary_key=True)
