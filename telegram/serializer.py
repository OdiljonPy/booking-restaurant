from rest_framework import serializers
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, MenuType, RestaurantMenu
from django.conf import settings


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


class TGRoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']

    def to_representation(self, instance):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', settings.MODELTRANSLATION_DEFAULT_LANGUAGE)
        if lang not in settings.MODELTRANSLATION_LANGUAGES:
            lang = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
        data = super().to_representation(instance)
        data['name'] = getattr(instance, 'name_' + lang)
        return data


class TGRestaurantRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description']


class TGMenuTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']


class TGRestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'description']
