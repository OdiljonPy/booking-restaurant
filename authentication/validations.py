import re
from django.core.exceptions import ValidationError

operators_code = ['88', '90', '91', '92', '93', '94', '95', '97', '98', '99', '55', '77']
"""
+99893 378 77 66
"""


def validate_uzb_number(value):
    if re.match('^\+998\d{9}$', value):
        return value
    else:
        raise ValidationError("Iltimos O'zbekiston telefon raqamini kiriting!")


def validate_uz_number(value):
    if value[:4] != "+998" or value[4:6] not in operators_code or len(value) != 13:
        raise ValidationError("Iltimos O'zbekistor raqamini kiriting!")