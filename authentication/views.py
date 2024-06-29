from datetime import timedelta, datetime
from django.contrib.auth import update_session_auth_hash
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenUser, Token
from django.contrib.auth.hashers import check_password, make_password
from authentication.models import User, OTP
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserSerializer, LoginSerializer, OTPSerializer, ChangePasswordSerializer, ResetUserPasswordSerializer,
    OTPUserPasswordSerializer, NewPasswordSerializer, OTPResendSerializer
)
from .utils import send_otp


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={201: openapi.Response(
            description='otp_key',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'otp_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='otp_key')}))})
    def create(self, request):
        data = request.data  # Post request
        user = User.objects.filter(username=data['username']).first()  # Is there a user or not?
        if user and user.is_verified:
            return Response(
                data={"message": "User already exists!", "ok": False},
                status=status.HTTP_400_BAD_REQUEST)
        if user:
            serializer = UserSerializer(user, data=data, partial=True)
        else:
            serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response({"message": serializer.errors, 'ok': False})
        user_validate = serializer.save()
        otp_all = OTP.objects.filter(user_id=user_validate.id)
        if otp_all and len(otp_all) >= 3 and otp_all.order_by('-created_at').first().created_at + timedelta(
                hours=12) > datetime.now():
            return Response(
                data={"error": "12 soatdan keyin urunib ko'ring!"},
                status=status.HTTP_400_BAD_REQUEST)
        otp = OTP.objects.create(user_id=user_validate.id)
        otp.save()
        send_otp(otp)
        return Response(
            data={"message": {'otp_key': otp.otp_key}, "ok": True},
            status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={200: openapi.Response(
            description='Successful',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='access_token'),
                    "refresh_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="refresh_token")}))},
    )
    def login(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user or not user.is_verified:
            return Response({'error': 'User not found', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(data['password'], user.password):
            # token = Token.for_user(request.user)
            # print(token.payload)
            # token.payload
            refresh = RefreshToken.for_user(user)

            access_token = str(refresh.access_token)
            return Response(
                data={'access_token': access_token, 'refresh_token': str(refresh)},
                status=status.HTTP_200_OK)
        return Response(
            data={'error': 'invalid password', 'ok': False},
            status=status.HTTP_400_BAD_REQUEST)


class OtpViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=OTPSerializer(),
        responses={200: openapi.Response(description='Successful')})
    def verify(self, request):
        data = request.data
        if not data.get('otp_code') is None or not data.get('otp_key') is None:
            otp = OTP.objects.filter(otp_key=data['otp_key']).first()
            if not otp:
                return Response(
                    data={'message': 'OTP not found', 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST, )
            if otp.created_at + timedelta(minutes=3) > datetime.now():
                return Response(
                    data={'message': 'OTP expired', 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST)
            if otp.attempts > 3:
                return Response(
                    data={"message": "Too many attempts! Try later after 12 hours.", 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST)
            if otp.otp_code != data['otp_code']:
                otp.attempts += 1
                otp.save(update_fields=['attempts'])
                return Response(
                    data={'message': 'OTP code mismatch', 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST)
            user = otp.user
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            OTP.objects.filter(user=user).delete()

            return Response(
                data={'message': 'Success', 'ok': True},
                status=status.HTTP_200_OK)
        return Response(
            data={'message': 'otp_code or otp_key not found', 'ok': False},
            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: openapi.Response(description='Successful')})
    def update(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Checking if old password is correct
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    data={'message': 'Old password is incorrect!', 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST)

            # Set password and save
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)  # Password Hashing

            return Response(
                data={'message': 'password successfully changed', 'ok': True},
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetUserPasswordSerializer,
        responses={201: openapi.Response(
            description='otp_key',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'otp_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='otp_key')}))})
    def reset(self, request):
        data = request.data['username']
        user = User.objects.filter(username=data).first()
        if not user or not user.is_verified:
            return Response(
                data={"message": "User not found!", "ok": False},
                status=status.HTTP_400_BAD_REQUEST)
        obj_all = OTP.objects.filter(user_id=user.id).order_by('-created_at')
        if not obj_all:
            return Response(
                data={"message": "You did not Register yet!", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)
        if len(obj_all) > 3 or datetime.now() - obj_all.first().created_at > timedelta(hours=12):
            return Response(
                data={'message': 'Too many attempts try after 12 hours', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)
        otp = OTP.objects.create(user_id=user.id)
        otp.save()
        send_otp(otp)
        return Response({"otp_key": otp.otp_key, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OTPUserPasswordSerializer,
        responses={200: openapi.Response(
            description='otp_token',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'otp_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='otp_token')}))})
    def verify(self, request):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        otp = OTP.objects.filter(otp_key=otp_key).first()
        if not otp:
            return Response(
                data={"message": "Otp_key wrong!", "ok": False},
                status=status.HTTP_400_BAD_REQUEST)
        if otp.attempts > 3:
            return Response(
                data={"message": "Too many attempts! Try later after 12 hours.", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)
        if otp.otp_code != otp_code:
            otp.attempts += 1
            return Response(
                data={"message": "otp_code is incorrect! Try again", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)
        otp.created_at += timedelta(minutes=3)
        otp.save()
        return Response({"otp_token": otp.otp_token, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=NewPasswordSerializer(),
        responses={200: openapi.Response(description='Successful')})
    def reset_new(self, request):
        token = request.data['otp_token']
        otp = OTP.objects.filter(otp_token=token).first()
        if not otp:
            return Response({'error': 'token is worst!'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=otp.user.username).first()
        if not user:
            return Response({"error": "user not exists", 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        if otp.created_at > datetime.now():
            return Response({'error': 'OTP expired', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(request.data['password'])
        user.save(update_fields=['password'])
        return Response({'ok': True}, status=status.HTTP_200_OK)


class OTPReset(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=OTPResendSerializer,
        responses={201: openapi.Response(
            description='otp_key',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'otp_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='otp_key')}))})
    def resend_otp(self, request):
        data = request.data
        obj = OTP.objects.filter(otp_key=data['otp_key']).first()
        if not obj:
            return Response({'message': 'Otp_key is wrong!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=obj.user.username).first()

        if user and user.is_verified:
            return Response({'massage': 'User already verified!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        obj_all = OTP.objects.filter(user=user).order_by('-created_at')
        if len(obj_all) > 3 or datetime.now() - obj_all.first().created_at > timedelta(minutes=1):
            return Response({'message': 'Too many attempts try after 12 hours', 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)
        new_otp = OTP.objects.create(user=obj.user)
        new_otp.save()
        send_otp(new_otp)
        return Response({'otp_key': new_otp.otp_key, 'ok': True}, status=status.HTTP_200_OK)
