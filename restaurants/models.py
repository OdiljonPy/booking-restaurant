from django.db import models
from authentication.models import User


class RestaurantCategory(models.Model):
    category_name = models.CharField(max_length=100)  # pan-asian, europe, usa, arabic, turkish, family
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Restaurant(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    restaurant_name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/restaurants/',
                                default='images/restaurants/default_restaurant.jpg')  # default= need to add
    description = models.TextField()
    service_fee = models.IntegerField()

    booking_count_total = models.IntegerField(default=0)
    booking_count_day_by_day = models.IntegerField(default=0)

    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=100)
    # location = models.CharField(max_length=100)

    category = models.ManyToManyField(RestaurantCategory, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name


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
    pictures = models.ImageField(upload_to='images/restaurants/room_images/',
                                 default='images/restaurants/room_images/default_room.jpg')  # default= need to add

    people_number = models.IntegerField(default=0)
    room_type = models.ManyToManyField(RoomType)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name


class MenuType(models.Model):
    type_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_name


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_type = models.ForeignKey(MenuType, models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    pictures = models.ImageField(upload_to='images/restaurants/menu_images/',
                                 default='images/restaurants/menu_images/default_menu.jpg')
    price = models.IntegerField(default=0)
    ingredients = models.TextField(max_length=2000)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    comment = models.TextField()
    is_visible = models.BooleanField(default=True)
    rating = models.IntegerField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.comment