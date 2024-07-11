from rest_framework import serializers
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, MenuType, RestaurantMenu


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['user_id', 'phone_number', 'username', 'first_name', 'last_name']


class TGRestaurantSerializer(serializers.ModelSerializer):  # Restaurant Serializer
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'phone', 'email', 'address']


class TGRestaurantCategorySerializer(serializers.ModelSerializer):  # Restaurant Category  Serializer
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['Restaurants'] = TGRestaurantSerializer(Restaurant.objects.filter(category_id=instance.id), many=True).data
        return data


class TGRoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']


class TGRestaurantRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description', 'pictures']


class TGMenuTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['restaurants'] = TGRestaurantSerializer(Restaurant.objects.filter(restaurant_id=instance.id),
                                                     many=True).data
        return data


class TGRestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'description']
