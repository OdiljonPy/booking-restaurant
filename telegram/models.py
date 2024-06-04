from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(default=0)
