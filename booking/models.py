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


status = {
    1: 'created',
    2: "paying",  # shu statuslarni xam korib qoyish kerak
    3: "paid",
    4: "booked",
    5: "cancelled",

}


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Restaurantni Room dan topsa boladi Room Restaurantga Foreign key qilingan - bu xozir admindan qoshgani turibdi
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)

    number_of_people = models.IntegerField(default=1)
    client_number = models.CharField(max_length=13)
    client_name = models.CharField(max_length=120)

    comment = models.TextField(blank=True, null=True)
    # Shu yerga Occasion ochirib tashlansa xam booking ochmashi kerak
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, blank=True, null=True, default=1)

    planed_from = models.DateTimeField(default=datetime.now)
    planed_to = models.DateTimeField(default=datetime.now)

    booked_time = models.DateTimeField(auto_now_add=True)

    order_items = models.ManyToManyField(OrderItems)
    # shu choice ni xam tekshirtirish kerak ekan adminkadan qoshganda
    # Select a valid choice. 1 is not one of the available choices. shu xatolikni chiqaryapti
    status = models.CharField(choices=status, default=1, max_length=10)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.restaurants.name


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
