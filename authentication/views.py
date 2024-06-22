from datetime import timedelta, datetime

from django.contrib.auth import update_session_auth_hash
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from authentication.models import User, OTP
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, LoginSerializer, OTPSerializer, ChangePasswordSerializer
from .utils import send_otp


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=UserSerializer())
    def create(self, request):
        data = request.data  # Post request
        user = User.objects.filter(username=data['username']).first()  # Is there a user or not?
        if user and user.is_verified:
            return Response({"error": "User already exists!", "ok": False}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            serializer = UserSerializer(user, data=data, partial=True)
        else:
            serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors, 'ok': False})
        user_validate = serializer.save()
        otp_all = OTP.objects.filter(user_id=user_validate.id)
        if otp_all and len(otp_all) >= 3 and otp_all.order_by('-created_at').first().created_at + timedelta(
                hours=12) > datetime.now():
            return Response({"error": "12 soatdan keyin urunib ko'r bratishka"})
        otp = OTP.objects.create(user_id=user_validate.id)
        otp.user.created_at += timedelta(minutes=1)
        otp.save()
        send_otp(otp)
        return Response({"result": {'otp_key': otp.otp_key}, "ok": True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={200: openapi.Response(
            description='Successful',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                  properties={
                                      'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                                     description='access_token'),
                                      "refresh_token": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      description="refresh_token")}))},
    )
    def login(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user or user.is_verified:
            return Response({'error': 'User not found', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response({'error': 'otp_code or otp_key not found', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)


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


class ResetPassword(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def reset(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user and not user.is_verified:
            return Response({"error": "User not found!", "ok": False})
        otp = OTP.objects.create(user_id=user.id)
        otp.save()
        send_otp(otp)
        return Response({"token": otp.otp_key, 'ok': True}, status=status.HTTP_200_OK)

    def verify(self, request):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        otp = OTP.objects.filter(otp_key=otp_key).first()
        if not otp:
            return Response({"error": "Otp_key wrong!", "ok": False}, status=status.HTTP_400_BAD_REQUEST)
        if otp.attempts >= 3:
            return Response({"error": "Too many attempts! Try later after 12 hours.", 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        if otp.otp_code != otp_code:
            otp.attempts += 1
            return Response({"error": "otp_code is incorrect! Try again", 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        otp.created_at += timedelta(minutes=3)
        otp.save()
        return Response({"Message": otp.otp_token, 'ok': True}, status=status.HTTP_200_OK)

    def reset_new(self, request):
        token = request.data['otp_token']
        otp_all = OTP.objects.filter(otp_token=token)
        if not otp_all:
            return Response({'error': 'token is worst!'}, status=status.HTTP_400_BAD_REQUEST)
        if otp_all and len(otp_all) >= 3 and otp_all.order_by('-created_at').first().created_at + timedelta(
                hours=12) > datetime.now():
            return Response({"error": "token is Trueexpired or to many attempts! Try after 12 hours", "ok": False},
                            status=status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        user = User.objects.filter(id=otp_all.first.user.id)
        print(user)
        user.password = make_password(password)
        user.save(update_fields=['password'])
        otp_all.delete()
        return Response({'ok': True}, status=status.HTTP_200_OK)
