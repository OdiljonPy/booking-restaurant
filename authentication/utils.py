import random
from django.conf import settings
import requests
from rest_framework.exceptions import ValidationError
from datetime import timedelta, datetime
from rest_framework import status


def generate_otp_code():
    first_digit = random.randint(1, 9)
    digits = [str(random.randint(0, 9)) for i in range(4)]
    return str(first_digit) + ''.join(digits)


def send_otp(otp):
    message = """
    Project: Booking Restaurants\nPhone_number: {}\nOTP_Code: {}\nOTP_Key: {}\nCreated_at: {}\nExpire_date : {}
    """.format(otp.user.username, otp.otp_code, otp.otp_key, otp.created_at, otp.created_at + timedelta(minutes=3))

    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))
    if status.status_code != 200:
        raise ValidationError("Texnik sabablarga ko'ra ko'd yuborilmadi, Iltimos keyinroq urinib ko'ring!")


def otp_expire(time):
    if datetime.now() - time < timedelta(minutes=3):
        return False
    return True


def check_otp(data):
    if len(data) > 3 or data.order_by('-created_at').first().created_at - datetime.now() > timedelta(hours=12):
        return True
    return False


def check_user(user):
    if user is None:
        raise ValidationError({"message": "User not found!", 'ok': False})
    if not user.is_verified:
        raise ValidationError({"message": "User is not verified!", "ok": False})
