from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username


