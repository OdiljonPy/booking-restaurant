from rest_framework import serializers
from .models import Manager, Administrator


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['user', 'phone_number', 'date_of_birth', 'hire_date', 'fire_date']


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ['user', 'phone_number', 'date_of_birth', 'hire_date']



class DateQuerySerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)


class DateRangeQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
    end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
