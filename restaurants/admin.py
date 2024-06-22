from django.contrib import admin
from .models import RestaurantCategory, Restaurant, RestaurantMenu, RestaurantRoom, RoomType  # RestaurantMenuItem

admin.site.register(RestaurantCategory)
admin.site.register(Restaurant)
admin.site.register(RestaurantMenu)
# admin.site.register(RestaurantMenuItem)
admin.site.register(RestaurantRoom)
admin.site.register(RoomType)
