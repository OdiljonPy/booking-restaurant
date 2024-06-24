from rest_framework import serializers
from booking.models import Booking
from restaurants.models import Restaurant
from .models import Manager, Employee
from authentication.models import User


class RestaurantSerializer(serializers.ModelSerializer):
    class RestaurantSerializer(serializers.ModelSerializer):
        class Meta:
            model = Restaurant
            fields = [
                'id', 'author', 'name', 'picture', 'description',
                'service_fee', 'booking_count_total', 'booking_count_day_by_day',
                'address', 'phone', 'email', 'category', 'created_at', 'updated_at'
            ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'author', 'restaurants', 'room', 'number_of_people', 'contact_number',
            'contact_username', 'comment','occasion', 'status', 'paying_status',
            'booked_time', 'planed_time'
        ]


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['title', 'phone_number', 'date_of_birth', 'hire_date', 'fire_date']
        read_only_fields = ['user']

        def save(self, **kwargs):
            user = self.context['request'].user
            my_user = User.objects.get(user=user)
            self.validated_data['user'] = my_user
            return super().save(**kwargs)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
