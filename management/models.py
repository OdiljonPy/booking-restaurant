from django.db import models
from datetime import datetime
from booking.models import STATUS_CHOICES
from authentication.models import User, validate_uz_number
from django.utils import timezone
from restaurants.models import Restaurant, RestaurantRoom,RoomType
from booking.models import  OrderItems,Occasion




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


class Booking(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room = models.ForeignKey(RestaurantRoom, on_delete=models.CASCADE)

    number_of_people = models.IntegerField(default=1)
    client_number = models.CharField(max_length=13)
    client_name = models.CharField(max_length=120)

    comment = models.TextField(blank=True, null=True)
    # Shu yerda Occasion ochirib tashlansa xam booking ochmashi kerak
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, blank=True, null=True, default=1)

    planed_from = models.DateTimeField(default=datetime.now)
    planed_to = models.DateTimeField(default=datetime.now)

    booked_time = models.DateTimeField(auto_now_add=True)

    order_items = models.ManyToManyField(OrderItems, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=1, max_length=10)
    total_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.client_name
