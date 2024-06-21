import uuid
from datetime import timedelta, datetime
from booking.models import Booking
from .utils import generate_otp_code, is_valid_uzbek_number, is_valid_pan, is_valid_year, is_valid_month
from django.db import models
from authentication.models import User
from restaurants.models import Restaurant


class Card(models.Model):
    pan = models.CharField(max_length=16, default=0, validators=[is_valid_pan])
    expire_month = models.CharField(max_length=2, default=0, validators=[is_valid_month])
    expire_year = models.IntegerField(default=0, validators=[is_valid_year])
    phone_number = models.CharField(max_length=13, validators=[is_valid_uzbek_number])
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pan


class OTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    phone_number = models.CharField(max_length=13, validators=[is_valid_uzbek_number])
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.expire_date = datetime.now() + timedelta(minutes=10)
        return super().save(force_insert, force_update, using, update_fields=update_fields)

    def __str__(self):
        return str(self.otp_key)


class PaymentWithHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_price = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='order_price')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.card.pan)
