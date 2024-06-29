from rest_framework import serializers
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, MenuType, RestaurantMenu


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'phone', 'username', 'first_name', 'last_name']


class RestSerializer(serializers.ModelSerializer):  # Restaurant Serializer
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'phone', 'email', 'address', 'category']


class ResCategorySerializer(serializers.ModelSerializer):  # Restaurant Category  Serializer
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['Restaurants'] = RestSerializer(Restaurant.objects.filter(category_id=instance.id), many=True).data
            return data


class RoomsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']


class RestaurantRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description', 'pictures']


class MenuTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['restaurants'] = RestSerializer(Restaurant.objects.filter(restaurant_id=instance.id), many=True).data
            return data


class RestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'description']
