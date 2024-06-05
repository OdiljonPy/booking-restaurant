from django.db import models
from ckeditor.fields import RichTextField
from authentication.models import User


class RestaurantCategory(models.Model):
    category_name = models.CharField(max_length=100)  # pan-asian, europe, usa, arabic, turkish, family
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Restaurant(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, null=True)  # need to discuss
    name = models.CharField(max_length=255)
    pictures = models.ImageField(upload_to='images/restaurants/')  # default= need to add
    description = models.TextField()
    service_fee = models.IntegerField()

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=100)

    category = models.ManyToManyField(RestaurantCategory)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    room_type_name = models.CharField(max_length=100)  # luxe, family, primary,

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_type_name


class RestaurantRoom(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    description = models.TextField()
    pictures = models.ImageField(upload_to='images/restaurants/room_images/')  # default= need to add

    people_number = models.IntegerField()
    waiters_number = models.IntegerField()
    room_type = models.ManyToManyField(RoomType)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name


class RestaurantMenu(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    ingredients = RichTextField(max_length=1000)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
