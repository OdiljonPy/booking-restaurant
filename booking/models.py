from datetime import datetime

from django.db import models

from authentication.models import User
from restaurants.models import Restaurant, RestaurantRoom, RestaurantMenu




class Occasion(models.Model):
    occasion_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.occasion_name

#TODO:need to add function calculate total price or fix exist function.
class OrderItems(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return self.menu.price * self.amount

    def __str__(self):
        return self.menu.name


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=1)
    contact_number = models.CharField(max_length=11)
    contact_username = models.CharField(max_length=120)
    comment = models.TextField(blank=True, null=True)
    occasion = models.ManyToManyField(Occasion, blank=True, null=True)
    booked_time = models.DateTimeField(auto_now_add=True)
    planed_time = models.DateTimeField(default=datetime.now)

    order_items = models.ForeignKey(OrderItems, on_delete=models.CASCADE)

    paying_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.restaurants.restaurant_name


class OrderFreeTable(models.Model):
    table_name = models.CharField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.table_name


class OrderFreeTime(models.Model):
    ordered_time = models.CharField(max_length=20)
    table = models.ForeignKey(OrderFreeTable, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ordered_time
