from django.core.exceptions import ValidationError
import re

"""
import random
import requests
from django.conf import settings
import re
from datetime import datetime, timedelta


# TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'
# BOT_TOKEN = '6387477042:AAEOg7Yz68zwD3YH9jWmwpij7SiUnki_O1E'
# CHANNEL_ID = '-1001973023371'


def generate_otp_code(*args, **kwargs):
    return random.randint(10000, 99999)


def send_otp(otp):
    message = "App: payment(card): \notp_code: {}\notp_key: {}\nphone_number: {}\ncreated_at: {}".format(
        otp.otp_code, otp.otp_key, otp.phone_number, otp.created_at)
    requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))



def is_valid_year(num):
    if 24 > num:
        raise ValidationError('Year should be greater then 24')


def is_valid_uzbek_number(phone_number):
    pattern = r'^(?:\+998|998)\d{9}$'card = models.ForeignKey(Card, on_delete=models.CASCADE)
    if not re.match(pattern, phone_number):
        raise ValidationError('You should enter an uzbek number')


def number_of_otp(otp):
    current_time = datetime.now()
    if len(otp) == 3:
        obj = otp[2]
        if current_time - obj.created_at < timedelta(hours=10):
            return False
        return 'delete'
    return True
"""


def pan_changer(pan):
    if len(pan) != 16:
        raise ValueError("Pan must be exactly 16 characters long.")
    first_four = pan[:4]
    middle_eight = '*' * 8
    last_four = pan[-4:]
    pan = first_four + middle_eight + last_four
    return pan


def is_valid_pan(pan):
    pattern = r'^(9860|8600)\*{8}\d{4}$'

    regex = re.compile(pattern)

    if not regex.match(pan):
        raise ValidationError('Pan is invalid')


def is_valid_month(month):
    pattern = r'^(0[1-9]|1[0-2])$'
    if not re.match(pattern, month):
        raise ValidationError('Month should be between one and twelve')
