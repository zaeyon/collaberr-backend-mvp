from django.core.validators import RegexValidator

class HexStringValidator(RegexValidator):

    def __init__(self, length: int):
        super().__init__(regex=r'^[0-9a-fA-F]{%d}$' % length,
                         message='Enter a valid hex string of length %d' % length,
                         code='invalid_hex_string')
