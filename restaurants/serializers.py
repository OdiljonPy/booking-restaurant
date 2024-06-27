from rest_framework.serializers import ModelSerializer
from .models import RestaurantCategory, Restaurant, RoomType, RestaurantRoom, RestaurantMenu, Comment, MenuType


class CategorySerializer(ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name']


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ['name']


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'author', 'name', 'description', 'picture', 'service_fee', 'balance', 'booking_count_total',
                  'booking_count_day_by_day', 'address', 'phone', 'email', 'category']


class RestaurantCreateSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['author', 'name', 'category']


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']


class RoomTypeCreateSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['name']


class RoomSerializer(ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description', 'restaurant', 'pictures', 'people_number', 'room_type']


class RoomCreateSerializer(ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['name', 'restaurant', 'people_number', 'room_type']


class MenuTypeSerializer(ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']


class MenuTypeCreateSerializer(ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['name']


class MenuSerializer(ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'restaurant', 'menu_type', 'description']


class MenuCreateSerializer(ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['name', 'restaurant', 'menu_type']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'restaurant', 'comment', 'menu', 'rating']


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['restaurant', 'menu', 'comment', 'rating']