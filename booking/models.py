from datetime import timezone

from django.db import models

from authentication.models import User
from restaurants.models import Restaurant, RestaurantRoom, RestaurantMenu


class Occasion(models.Model):
    occasion_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.occasion_name


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_time = models.DateTimeField(auto_now_add=True)
    planed_time = models.DateTimeField(default=timezone.now)
    restaurants = models.ManyToManyField(Restaurant)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=1)
    meals = models.ManyToManyField(RestaurantMenu, blank=True, null=True)
    contact_number = models.CharField(max_length=11)
    contact_username = models.CharField(max_length=120)
    comment = models.TextField(blank=True, null=True)
    occasion = models.ManyToManyField(Occasion, blank=True, null=True)

    def __str__(self):
        return self.restaurants.name

