import re
from django.core.exceptions import ValidationError

operators_code = ['88', '90', '91', '92', '93', '94', '95', '97', '98', '99', '55', '77']
"""
+99893 378 77 66
"""


def validate_uz_number(value):
    if re.match('^\+998\d{9}$', value) and value[4, 6] not in operators_code:
        raise ValidationError("Iltimos O'zbekistor raqamini kiriting!")
