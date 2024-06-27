import uuid

from .utils import is_valid_pan, is_valid_month
from django.db import models

"""
from ..authentication.models import User
from ..restaurants.models import Restaurant
from ..booking.models import Booking
"""

FAILED, PAYED, RETURNED, DO_NOT_PAYED_YET = ('failed', 'payed', 'returned', 'do_not_payed_yet')


"""
class Card(models.Model, BaseModel):
    pan = models.CharField(max_length=16, default=0, validators=[is_valid_pan])
    expire_month = models.CharField(max_length=2, default=0, validators=[is_valid_month])
    expire_year = models.IntegerField(default=0, validators=[is_valid_year])
    phone_number = models.CharField(max_length=13, validators=[is_valid_uzbek_number])
    card_holder = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.pan


class OTP(models.Model, BaseModel):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
"""


class PaymentWithHistory(models.Model):
    STATUS_CHOICES = (
        ('1', DO_NOT_PAYED_YET),
        ('2', PAYED),
        ('3', FAILED),
        ('4', RETURNED)
    )
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    pan = models.CharField(max_length=16, validators=[is_valid_pan])
    expire_month = models.CharField(max_length=2, validators=[is_valid_month])
    amount = models.FloatField()
    status = models.CharField(max_length=21, choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)


"""

payment:

1) post
2) add card
3) remove card

"""
