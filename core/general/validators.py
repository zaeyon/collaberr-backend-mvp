from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class HexStringValidator(RegexValidator):
    def __init__(self, length: int):
        super().__init__(regex=r'^[0-9a-fA-F]{%d}$' % length,
                         message='Enter a valid hex string of length %d' % length,
                         code='invalid_hex_string')


class PasswordValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(_("The password must contain at least one uppercase letter."))
        if not any(char.islower() for char in password):
            raise ValidationError(_("The password must contain at least one lowercase letter."))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("The password must contain at least one digit."))
        if not any(not char.isalnum() for char in password):
            raise ValidationError(_("The password must contain at least one special character."))

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
