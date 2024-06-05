from rest_framework.serializers import ModelSerializer
from .models import RestaurantCategory, Restaurant


class CategorySerializer(ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = "__all__"


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
