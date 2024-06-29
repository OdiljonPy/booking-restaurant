from django.db import models
from authentication.validations import validate_uz_number


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=14, validators=[validate_uz_number], blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
