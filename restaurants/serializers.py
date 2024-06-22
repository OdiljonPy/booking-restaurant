from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import RestaurantCategory, Restaurant, RoomType, RestaurantRoom, RestaurantMenu, Comment, MenuType, \
    RestaurantMenuItem


class CategorySerializer(ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name']


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'author', 'name', 'description', 'picture', 'service_fee', 'balance', 'booking_count_total',
                  'booking_count_day_by_day', 'address', 'phone', 'email', 'category']


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']


class RoomSerializer(ModelSerializer):
    class Meta:
        model = RestaurantRoom
        fields = ['id', 'name', 'description', 'restaurant', 'pictures', 'people_number', 'room_type']


class MenuTypeSerializer(ModelSerializer):
    class Meta:
        model = MenuType
        fields = ['id', 'name']


class MenuSerializer(ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'restaurant', 'menu_type', 'description']


class RestaurantMenuItemSerializer(ModelSerializer):
    class Meta:
        model = RestaurantMenuItem
        fields = ['id', 'restaurant_menu', 'name', 'description', 'pictures', 'ingredients', 'price']

#TODO: need to discuss
class CommentSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(write_only=True)
    menu_name = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['restaurant_name', 'menu_name', 'comment', 'rating']
        extra_kwargs = {
            'user': {'read_only': True},
            'rating': {'required': True}
        }

    def create(self, validated_data):

        restaurant_name = validated_data.pop('restaurant_name')
        menu_name = validated_data.pop('menu_name')

        try:
            restaurant = Restaurant.objects.get(restaurant_name=restaurant_name)
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError("No restaurant with the specified name was found.")

        try:
            menu = RestaurantMenu.objects.get(menu_name=menu_name)
        except RestaurantMenu.DoesNotExist:
            raise serializers.ValidationError("The menu item with the specified name was not found.")

        user = self.context['request'].user

        comment = Comment.objects.create(user=user, restaurant=restaurant, menu=menu, **validated_data)
        return comment
