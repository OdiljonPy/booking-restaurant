import re
from django.core.exceptions import ValidationError


def validate_uzb_number(value):
    if re.match('^\+998\d{9}$', value):
        return value
    else:
        raise ValidationError("Iltimos O'zbekiston telefon raqamini kiriting!")
