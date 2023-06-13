from django.db import models
from django.conf import settings

from core.general.models import CreatedModified
from core.general.validators import HexStringValidator
from core.general.constants import ID_LENGTH, USER_NAME_LENGTH

class Campaign(CreatedModified):
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        db_table = 'campaigns'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.CharField(max_length=100)
    description = models.TextField()
    username = models.CharField(max_length=USER_NAME_LENGTH)

    def __str__(self):
        return f'{self.title} | {self.username}'
    
