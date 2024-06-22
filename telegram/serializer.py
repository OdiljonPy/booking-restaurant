from rest_framework import serializers
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, MenuType, RestaurantMenu


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['user_id', 'first_name', 'last_name', 'username']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'phone', 'email', 'address']


class ResCategorySerializer(serializers.ModelSerializer):  # Restaurant Category  Serializer
    class Meta:
        model = RestaurantCategory
        fields = ['name']


class RoomsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['name']


class RestaurantRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['name', 'description', 'pictures']


class MenuTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['name']


class RestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['name', 'description']
