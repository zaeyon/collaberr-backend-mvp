from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator

from core.general.models import CreatedModified
from core.general.constants import USER_NAME_LENGTH


class Campaign(CreatedModified):
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        db_table = 'campaigns'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.TextField(validators=[MaxLengthValidator(100)])
    description = models.TextField()
    username = models.TextField(validators=[MaxLengthValidator(USER_NAME_LENGTH)])

    def __str__(self):
        return f'{self.title} | {self.username}'
