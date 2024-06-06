import uuid
from datetime import timedelta, datetime

from .utils import generate_otp_code
from django.db import models


class Cards(models.Model):
    pan = models.IntegerField(default=0, validators=[])
    expire_month = models.IntegerField(default=0, validators=[])
    expire_year = models.IntegerField(default=0, validators=[])
    phone_number = models.IntegerField(max_length=12, validators=[])
    owner_name = models.CharField(max_length=120, validators=[])
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_name


class OTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    phone_number = models.CharField(max_length=12, validators=[])
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.expire_date = datetime.now() + timedelta(minutes=10)
        return super().save(force_insert, force_update, using, update_fields=update_fields)

    def __str__(self):
        return str(self.otp_key)


class Booking(models.Model):
    pass
