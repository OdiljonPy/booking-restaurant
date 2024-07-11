import requests
from django.conf import settings


def telegram_add(telegramuser):
    message = ("""Successfully!!!\ntelegram_id: {}\nfirst_name: {}\nlast_name: {}\nphone_number: {}\nusername: {}""".format(
        telegramuser.user_id,
        telegramuser.first_name,
        telegramuser.last_name,
        telegramuser.phone_number, telegramuser.username))
    requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))
