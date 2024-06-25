from rest_framework import serializers
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, MenuType, RestaurantMenu


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['user_id', 'first_name', 'last_name', 'username', 'phone']


class AllRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']


class RestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'phone', 'email', 'address']


class ResCategorySerializer(serializers.ModelSerializer):  # Restaurant Category  Serializer
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name']


class RoomsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']


class RestaurantRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description', 'pictures']


class MenuTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']


class RestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'description']
