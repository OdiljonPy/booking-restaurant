from .utils import is_valid_pan, is_valid_month, is_valid_amount
from django.db import models
from .utils import mask_pan


FAILED, PAYED, RETURNED, DO_NOT_PAYED_YET = ('failed', 'payed', 'returned', "don't payed yet")


class PaymentWithHistory(models.Model):
    STATUS_CHOICES = (
        (1, DO_NOT_PAYED_YET),
        (2, PAYED),
        (3, FAILED),
        (4, RETURNED)
    )
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, blank=True,
                                null=True)  # need to delete ' blank=True, null=True ' after booking changed.
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    pan = models.CharField(max_length=16, validators=[is_valid_pan])
    expire_month = models.CharField(max_length=2, validators=[is_valid_month])
    amount = models.FloatField(validators=[is_valid_amount])
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pan = mask_pan(self.pan)
        super(PaymentWithHistory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)
