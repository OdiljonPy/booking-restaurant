from rest_framework.exceptions import ValidationError as ValidationErrorViews
from django.core.exceptions import ValidationError
import re

"""
def is_valid_year(num):
    if 24 > num:
        raise ValidationError('Year should be greater then 24')
"""


def pan_checker(pan):
    if pan is None:
        raise ValidationErrorViews("Pan is mandatory field!")


def booking_checker(booking_id):
    if booking_id is None or not booking_id.isnumeric():
        raise ValidationErrorViews("booking_id is required field! and should be integer number")


def is_valid_pan(pan):
    pattern = r'^(9860|8600)\d{12}$'
    regex = re.compile(pattern)
    if not regex.match(pan):
        raise ValidationError('Pan is invalid')


def is_valid_month(month):
    pattern = r'^(0[1-9]|1[0-2])$'
    if not re.match(pattern, month):
        raise ValidationError('Month should be between one and twelve || like <01 .. 12>')


def is_valid_amount(amount):
    if amount <= 0:
        raise ValidationError('Amount should be greater than 0.00')


def mask_pan(pan):
    first_four = pan[:4]
    middle_eight = '*' * 8
    last_four = pan[-4:]
    covered_pan = first_four + middle_eight + last_four
    return covered_pan


def mask_user(username):
    first_six = username[:6]
    middle_five = '*' * 5
    last_two = username[-2:]
    covered_username = first_six + middle_five + last_two
    return covered_username

