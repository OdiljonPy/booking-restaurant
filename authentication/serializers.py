from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'date_joined',
                            'is_staff', 'is_superuser',
                            'groups', 'user_permissions', 'is_active'
                            )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        print(self.validated_data)
        self.validated_data['password'] = make_password(self.validated_data['password'])
        print(self.validated_data)
        return super().save(**kwargs)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(validated_data['username'], validated_data['password'])
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
