import random


import requests

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"
BOT_TOKEN = "6787403849:AAE2piymBY7F-9DCRKbEK3kZoBx1paVSTog"
CHANNEL_ID = "-1002188042090"


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

    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))


