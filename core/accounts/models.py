from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.general.validators import HexStringValidator
from core.general.constants import ACCOUNT_ID_LENGTH
from .managers import AccountManager

class Account(AbstractBaseUser):
    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    account_id = models.CharField(
            max_length=ACCOUNT_ID_LENGTH,
            primary_key=True,
            validators=[HexStringValidator(ACCOUNT_ID_LENGTH)],
            )
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=25)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'{self.username} | {self.balance}'

    @property
    def id(self):
        return self.account_id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    # for businesses
    # for creators
    # earnings = models.PositiveIntegerField(default=0, )


    
