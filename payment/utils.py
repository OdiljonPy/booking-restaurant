import random
import requests
from config.settings import TELEGRAM_API_URL, BOT_TOKEN, CHANNEL_ID
import re


# TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'
# BOT_TOKEN = '6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE'
# CHANNEL_ID = '-1002048118873'


def generate_otp_code(*args, **kwargs):
    return random.randint(10000, 99999)


def send_otp(otp):
    message = """App: payment(card): \notp_code: {}\notp_key\nphone_number: {}\ncreated_at: {}""".format(
        otp.otp_code, otp.otp_key, otp.phone_number, otp.created_at)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))


def is_valid_pan(pan):
    pattern = r'^(8600|9860)\d{12}$'
    if re.match(pattern, pan):
        return True
    else:
        return False


def is_valid_month(month):
    pattern = r'^(0[1-9]|1[0-2])$'
    if re.match(pattern, month):
        return True
    else:
        return False


def is_valid_year(year):
    pattern = r'^(202)\d{1}$'
    if re.match(pattern, year):
        return True
    else:
        return False


def is_valid_uzbek_number(phone_number):
    pattern = r'^(?:\+998|998)\d{9}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False
