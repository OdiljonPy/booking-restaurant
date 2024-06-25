from django.db import models
from booking.models import Booking


class PaymentHistory(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED'
        PENDING = 'PENDING'
        PAID = 'PAID'
        CANCELED = 'CANCELED'

    order = models.OneToOneField(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.author.user.username
