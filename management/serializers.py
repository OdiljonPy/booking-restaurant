from rest_framework import serializers
from booking.models import Booking
from restaurants.models import Restaurant
from .models import Manager, Booking_costumer
from authentication.models import User


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['user', 'title', 'phone_number', 'date_of_birth', 'hire_date', 'fire_date']




class  BookingCostumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_costumer
        fields = '__all__'

class DateQuerySerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)


class DateRangeQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
    end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
