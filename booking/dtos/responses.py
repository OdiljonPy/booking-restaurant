from rest_framework import serializers

from booking.models import Booking, Occasion, OrderItems
from booking.serializers import OrderItemsSerializer, OrderSerializer


# INFO: This serializers used on swaggers
class OrderItemsResponseSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ['menu', 'amount', 'total_price']

    def get_total_price(self, obj):
        return obj.calculate_total_price()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        menu = instance.menu


class BookingResponseSerializer(serializers.ModelSerializer):
    # order_items = OrderItemsSerializer(many=True)

    class Meta:
        model = Booking
        fields = ['id', 'author', "restaurants", 'room', 'number_of_people', 'client_number', 'client_name',
                  'planed_from', 'planed_to', "occasion", "status"]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     order_items = instance.order_items.all()
    #     data['orders'] = OrderSerializer(order_items, many=True).data
    #     return data

    # def save(self, **kwargs):
    #     request = self.context['request']
    #     # request tookendan oladi shuning uchun token qoshilmasa {"author":["This field is required."]}
    #     user = User.objects.filter(user_id=request.user.id).first()
    #     self.validated_data['author'] = user
    #     return super().save(**kwargs)


class OccasionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'name', ]


class PayingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking

    fields = ['author', "restaurants", 'client_name', "total_sum"]
