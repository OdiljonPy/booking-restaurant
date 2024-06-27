from rest_framework.exceptions import ValidationError
import re


def name_validator(name):
    if len(name) > 1:
        return name
    else:
        raise ValidationError('Name must have at least one character')


def validate_uzb_number(number):
    if re.match('^\+998\d{9}$', number):
        return number
    else:
        raise ValidationError('Please enter a valid UZB number')