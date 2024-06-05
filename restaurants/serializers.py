from rest_framework.serializers import ModelSerializer
from .models import RestaurantCategory, Restaurant, RoomType, RestaurantRoom


class CategorySerializer(ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = "__all__"


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = "__all__"
