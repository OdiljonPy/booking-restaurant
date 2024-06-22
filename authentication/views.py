from datetime import timedelta, datetime

from django.contrib.auth import update_session_auth_hash
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from authentication.models import User, OTP
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer, OTPSerializer, ChangePasswordSerializer
from .utils import send_otp, generate_otp_code


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=UserSerializer())
    def create(self, request):
        data = request.data  # Post request
        user = User.objects.filter(username=data['username']).first()
        print(user)# Is there a user or not?
        if not user:  # if not user in database
            serializer = UserSerializer(data=data)  # User creating
            if serializer.is_valid():
                user_validate = serializer.save()
                otp = OTP.objects.create(user_id=user_validate.id, otp_code=generate_otp_code())
                otp.expire_data = otp.created_at + timedelta(minutes=1)
                otp.save()
                send_otp(otp)
                return Response({'result': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors})

        if user and not user.is_verified:  # There is a user but not verified
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                user_validate = serializer.save()  # Update and create a new otp
                otp = OTP.objects.create(user_id=user_validate.id, otp_code=generate_otp_code())
                otp.expire_data = otp.created_at + timedelta(minutes=1)
                otp.save()
                send_otp(otp)
                return Response({'result': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={200: openapi.Response(description='Successful',
                                         schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                             'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                                            description='access_token'),
                                             "refresh_token": openapi.Schema(type=openapi.TYPE_STRING,
                                                                             description="refresh_token")}))},
    )
    def login(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return Response({'error': 'User not found', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response({'error': 'User does not exists', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(data['password'], user.password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'error': 'invalid password', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)


class OtpViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=OTPSerializer(),

    )
    def verify(self, request):
        data = request.data
        if not data.get('otp_code') is None or not data.get('otp_key') is None:
            otp = OTP.objects.filter(otp_key=data['otp_key']).first()
            if not otp:
                return Response({'error': 'OTP not found', 'ok': False}, status=status.HTTP_400_BAD_REQUEST, )
            if otp.user.created_at > datetime.now():
                return Response({'error': 'OTP expired', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
            if otp.otp_code != data['otp_code']:
                return Response({'error': 'OTP code mismatch', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
            user = otp.user
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            otp.delete()
            return Response({'result': 'Success', 'ok': True}, status=status.HTTP_200_OK)
        return Response({'error': 'otp_code and otp_key not', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def update(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Checking if old password is correct
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Old password is incorrect.'], 'ok': False},
                                status=status.HTTP_400_BAD_REQUEST)

            # Set password and save
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)  # Password Hashing

            return Response({'status': 'password successfully changed', 'ok': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)