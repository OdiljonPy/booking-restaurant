from django.db import models
from datetime import datetime
from authentication.models import User, validate_uz_number
from django.utils import timezone
from restaurants.models import Restaurant, RestaurantRoom, RoomType
from booking.models import OrderItems, Occasion


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
