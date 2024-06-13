import random
import requests
from config.settings import TELEGRAM_API_URL, BOT_TOKEN, CHANNEL_ID

# TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'
# BOT_TOKEN = '6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE'
# CHANNEL_ID = '-1002048118873'


def generate_otp_code(*args, **kwargs):
    return random.randint(10000, 99999)


def send_otp(otp):
    message = """App: payment(card): \notp_code: {}\notp_key\nphone_number: {}\ncreated_at: {}""".format(
        otp.otp_code, otp.otp_key, otp.phone_number, otp.created_at)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))


def uzb_number(number):
    # number = args['number']
    if (len(number) == 13 and number[0] == '+' and number[1:].isnumeric() and number[1] == 9 and number[2] == 9 and
            number[3] == 8 or len(number) == 12 and number.isnumeric() and number[0] == 9 and number[1] == 9 and
            number[2] == 8):
        return {'message': number}
    return {'message': 'Your number is not uzbek number'}


def pan_number(pan):
    # pan = args['pan']
    try:
        pan = int(pan)
    except Exception:
        return {'message': 'Your pan is invalid'}
    if len(pan) == 16:
        return {'message': pan}


def month_valid(month):
    # month = args['month']
    if len(month) == 2 and ((month[0] == 0 and month[1] <= 2) or month <= 12):
        return {'message': month}
    return {'message': 'Month is invalid'}


def year_valid(year):
    # year = args['year']
    try:
        year = int(year)
    except Exception:
        return {'message': 'Year is invalid'}
    if year.isnumeric() and year >= 24 and year <= 30:
        return {'message': year}

