from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Booking, Occasion, OrderFreeTable, OrderFreeTime

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = '__all__'


class OrderFreeTableSerializer(ModelSerializer):
    class Meta:
        model = OrderFreeTable
        fields = '__all__'


class OrderFreeTimeSerializer(ModelSerializer):
    class Meta:
        model = OrderFreeTime
        fields = '__all__'
