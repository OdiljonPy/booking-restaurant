from datetime import datetime

from django.db import models

from authentication.models import User
from restaurants.models import Restaurant, RestaurantRoom, RestaurantMenu

STATUS_CHOICES = (
    (1, 'CREATED'),
    (2, 'PAYING'),
    (3, 'PAID'),
    (4, 'BOOKED'),
    (5, 'CANCELLED'),
)


class Occasion(models.Model):
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# TODO:need to add function calculate total price or fix exist function.
class OrderItems(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return self.menu.price * self.amount

    def __str__(self):
        return self.menu.name


class Order(models.Model):
    order_items = models.ManyToManyField(OrderItems, blank=True)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room.name


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)

    number_of_people = models.IntegerField()
    client_number = models.CharField(max_length=13)
    client_name = models.CharField(max_length=120)

    comment = models.TextField(blank=True, null=True)
    # Shu yerda Occasion ochirib tashlansa xam booking ochmashi kerak
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, blank=True, null=True, default=1)

    planed_from = models.DateTimeField(default=datetime.now)
    planed_to = models.DateTimeField(default=datetime.now)

    booked_time = models.DateTimeField(auto_now_add=True)

    orders = models.ManyToManyField(Order, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=1, max_length=10)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.client_name
