from django.contrib import admin
from .models import RestaurantCategory, Restaurant, RestaurantMenu, RestaurantRoom, RoomType, \
    MenuType, Comment


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


admin.site.register(RestaurantMenu)
admin.site.register(RestaurantRoom)
admin.site.register(RoomType)
admin.site.register(MenuType)
admin.site.register(Comment)
