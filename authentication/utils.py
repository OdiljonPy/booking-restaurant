import random
import re

import requests
from rest_framework.exceptions import ValidationError

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"
BOT_TOKEN = "6787403849:AAE2piymBY7F-9DCRKbEK3kZoBx1paVSTog"
CHANNEL_ID = "-1002188042090"


def generate_otp_code(*args, **kwargs):
    return random.randint(100000, 999999)


def send_otp(otp):
    message = """
    Platform: Booking Restaurants
    Phone_number: {}
    OTP_Code: {}
    OTP_Key: {}
    Created_at: {}
    Expire_date : {}
    """.format(otp.user.username, otp.otp_code, otp.otp_key, otp.created_at, otp.expire_data)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))


def validate_uz_number(value):
    if re.match('^\+998\d{9}$', value):
        return value
    else:
        raise ValidationError("Iltimos O'zbekiston telefon raqamini kiriting!")
