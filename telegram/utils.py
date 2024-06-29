import requests
from config.settings import TELEGRAM_API_URL, BOT_TOKEN, CHANNEL_ID


def telegram_add(telegramuser):
    message = """Successfully!!!\ntelegram_id: {}\nfirst_name: {}\nlast_name: {}\nphone: {}\nusername: {}""".format(
        telegramuser.telegram_id,
        telegramuser.first_name,
        telegramuser.last_name,
        telegramuser.phone, telegramuser.username)
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHANNEL_ID))
