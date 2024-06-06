import random
import requests

TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}'
BOT_TOKEN = '6387477042:AAEOg7Yz68zwD3YH9jWmwpij7SiUnki_O1E'
CHANNEL_ID = '-1001973023371'

def generate_otp_code(*args, **kwargs):
    return random.randint(10000, 99999)


def send_otp(otp):
    message = """App: payment(card): \notp_code: {}\notp_key\nphone_number: {}\ncreated_at: {}""".format(
        otp.otp_code, otp.otp_key, otp.phone_number, otp.created_at)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))