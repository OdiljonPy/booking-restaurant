from django.db import models
from datetime import datetime

from authentication.models import User, validate_uz_number
from django.utils import timezone
from restaurants.models import *


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.title}'
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, validators=[validate_uz_number])
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(default=timezone.now)
    fire_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username




class Occasion_costumer(models.Model):
    occasion_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.occasion_name


class OrderItems_costumer(models.Model):
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return self.menu.price * self.amount

    def __str__(self):
        return self.menu.name


class Booking_costumer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=1)
    contact_number = models.CharField(max_length=11)
    contact_username = models.CharField(max_length=120)
    comment = models.TextField(blank=True, null=True)
    occasion = models.ManyToManyField(Occasion_costumer)
    booked_time = models.DateTimeField(auto_now_add=True)
    planed_time = models.DateTimeField(default=datetime.now)

    order_items = models.ForeignKey(OrderItems_costumer, on_delete=models.CASCADE)

    paying_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.restaurants.restaurant_name
