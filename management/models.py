from django.db import models
from datetime import datetime

from authentication.models import User, validate_uz_number
from django.utils import timezone
from restaurants.models import Restaurant, RoomType, RestaurantRoom
from booking.models import Occasion, OrderItems

STATUS_CHOICES = [
    ('1', 'created'),
    ('2', 'paying'),
    ('3', 'paid'),
    ('4', 'booked'),
    ('5', 'cancelled'),
]


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, validators=[validate_uz_number])
    date_of_birth = models.DateField(default=datetime.now)
    hire_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class BookingCustomer(models.Model):
    author = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=11, validators=[validate_uz_number])
    comment = models.TextField(default="No comment")
    booked_time = models.DateTimeField(auto_now_add=True)
    planed_time = models.DateTimeField(default=datetime.now)
    order_items = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    paying_status = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default=1, max_length=10)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.restaurant.name
