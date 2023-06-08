from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.project.validators import HexStringValidator
from core.project.constants import ACCOUNT_NUMBER_LENGTH

class Account(AbstractBaseUser, PermissionsMixin):
    account_number = models.CharField(
            max_length=ACCOUNT_NUMBER_LENGTH,
            primay_key=True,
            validators=[HexStringValidator(ACCOUNT_NUMBER_LENGTH)],
            )



