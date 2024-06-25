from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from .models import Booking, Occasion, OrderFreeTable, OrderFreeTime, OrderItems
from restaurants.serializers import MenuSerializer


class OrderItemsSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ['menu', 'amount', 'total_price']

    def get_total_price(self, obj):
        return obj.calculate_total_price()


class BookingSerializer(serializers.ModelSerializer):
    # order_items = OrderItemsSerializer(many=True)

    class Meta:
        model = Booking
        fields = ['author', 'room', "restaurants", 'number_of_people', 'client_number', 'client_name', 'planed_from',
                  'planed_to', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        order_items = instance.order_items.all()
        data['order_items'] = OrderItemsSerializer(order_items, many=True).data
        return data

    # def save(self, **kwargs):
    #     request = self.context['request']
    #     # request tookendan oladi shuning uchun token qoshilmasa {"author":["This field is required."]}
    #     user = User.objects.filter(user_id=request.user.id).first()
    #     self.validated_data['author'] = user
    #     return super().save(**kwargs)


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['name', ]


class OrderFreeTableSerializer(ModelSerializer):
    class Meta:
        model = OrderFreeTable
        fields = '__all__'


class OrderFreeTimeSerializer(ModelSerializer):
    class Meta:
        model = OrderFreeTime
        fields = '__all__'
