import random
from django.conf import settings
import requests
from .exceptions import BadRequestException


def generate_otp_code():
    return random.randint(10000, 99999)


def send_otp(otp):
    message = """
    Platform: Booking Restaurants
    Phone_number: {}
    OTP_Code: {}
    OTP_Key: {}
    Created_at: {}
    Expire_date : {}
    """.format(otp.user.username, otp.otp_code, otp.otp_key, otp.created_at, otp.user.created_at)

    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))
    if status.status_code != 200:
        raise BadRequestException("Texnik sabablarga ko'ra ko'd yuborilmadi, Iltimos keyinroq urinib ko'ring!")
