from rest_framework import serializers
from .models import Manager, BookingCustomer
from authentication.models import User


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['user',  'phone_number', 'date_of_birth', 'hire_date', 'fire_date']


class BookingCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCustomer
        fields = '__all__'


class DateQuerySerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)


class DateRangeQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
    end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
