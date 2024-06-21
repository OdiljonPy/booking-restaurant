from django.contrib import admin
from .models import RestaurantCategory, Restaurant, RestaurantMenu, RestaurantMenuItem, RestaurantRoom, RoomType

admin.site.register(RestaurantCategory)
admin.site.register(Restaurant)
admin.site.register(RestaurantMenu)
admin.site.register(RestaurantMenuItem)
admin.site.register(RestaurantRoom)
admin.site.register(RoomType)

