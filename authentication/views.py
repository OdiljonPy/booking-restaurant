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
from .serializers import (
    UserSerializer, LoginSerializer, OTPSerializer, ChangePasswordSerializer, ResetUserPasswordSerializer,
    OTPUserPasswordSerializer, NewPasswordSerializer, OTPResendSerializer
)
from .utils import send_otp, otp_expire, check_otp, check_user


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={
            201: openapi.Response(
                description='otp_key',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'otp_key': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='otp_key'
                        )
                    }
                )
            )
        }
    )
    def register(self, request):
        data = request.data  # Post request
        obj_user = User.objects.filter(username=data['username']).first()  # Is there a user or not?

        if obj_user and obj_user.is_verified:
            return Response(
                data={"message": "User already exists!", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(obj_user, data=data, partial=True) if obj_user else UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data={"message": serializer.errors, 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_user = serializer.save()
        obj_create = OTP.objects.create(user_id=validated_user.id)
        obj_all = OTP.objects.filter(user_id=validated_user.id)

        if check_otp(obj_all):
            return Response(
                data={"message": "Too many attempts try after 12 hours"},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj_create.save()
        send_otp(obj_create)
        return Response(data={"message": {'otp_key': obj_create.otp_key}, "ok": True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={
            200: openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='access_token'
                        ),
                        'refresh_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='refresh_token'
                        )
                    }
                )
            )
        }
    )
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response(
                data={'message': 'Please write fill all planks!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        obj_user = User.objects.filter(username=username).first()

        check_user(obj_user)

        if check_password(password, obj_user.password):
            refresh = RefreshToken.for_user(obj_user)
            access_token = str(refresh.access_token)
            return Response(
                data={'access_token': access_token, 'refresh_token': str(refresh)},
                status=status.HTTP_200_OK)

        return Response(
            data={'message': 'User not found or password incorrect!', 'ok': False},
            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=OTPSerializer(),
        responses={200: openapi.Response(description='Success')})
    def verify(self, request):
        otp_code = request.data.get('otp_code')
        otp_key = request.data.get('otp_key')

        if otp_code is None or otp_key is None:
            return Response(
                data={'message': 'OTP code or key not found', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        obj_otp = OTP.objects.filter(otp_key=otp_key).first()

        if obj_otp is None:
            return Response(
                data={'message': 'OTP not found', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        if otp_expire(obj_otp.created_at):
            return Response(
                data={'message': 'OTP expired!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        if obj_otp.attempts > 3:
            return Response(
                data={"message": "Too many attempts! Try later after 12 hours.", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        if obj_otp.otp_code != otp_code:
            obj_otp.attempts += 1
            obj_otp.save(update_fields=['attempts'])
            return Response(
                data={'message': 'OTP code is incorrect!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        user = obj_otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        OTP.objects.filter(user=user).delete()
        return Response(data={'message': 'OTP verification successful', 'ok': True}, status=status.HTTP_200_OK)


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
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetUserPasswordSerializer,
        responses={
            201: openapi.Response(
                description='otp_key',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'otp_key': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='otp_key'
                        )
                    }
                )
            )
        }
    )
    def reset(self, request):
        username = request.data.get('username')
        if not username:
            return Response(
                data={"message": "Please fill the blank!", "ok": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()

        check_user(user)  # it will check user
        obj_create = OTP.objects.create(user_id=user.id)
        obj_create.save()
        send_otp(obj_create)
        return Response({"otp_key": obj_create.otp_key, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OTPUserPasswordSerializer,
        responses={
            200: openapi.Response(
                description='otp_token',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'otp_token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='otp_token'
                        )
                    }
                )
            )
        }
    )
    def verify(self, request):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')
        if not otp_key or not otp_code:
            return Response(
                data={'message': 'OTP code or key wrong!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = OTP.objects.filter(otp_key=otp_key).first()

        if otp is None:
            return Response(
                data={"message": "Invalid OTP key!", "ok": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.attempts > 3:
            return Response(
                data={"message": "Too many attempts! Try later after 12 hours.", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.otp_code != otp_code:
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            return Response(
                data={"message": "Incorrect OTP code! Try again.", 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"otp_token": otp.otp_token, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=NewPasswordSerializer(),
        responses={200: openapi.Response(description='Successful')})
    def reset_new(self, request):
        token = request.data.get('otp_token')
        new_password = request.data.get('password')

        if not token or not new_password:
            return Response(
                data={'message': 'Please fill all blanks!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj_otp = OTP.objects.filter(otp_token=token).first()

        if obj_otp is None:
            return Response({'error': 'Invalid OTP token!'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_expire(obj_otp.created_at):
            return Response({'error': 'OTP expired!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        user = obj_otp.user
        user.password = make_password(new_password)
        user.save(update_fields=['password'])
        OTP.objects.filter(otp_token=token).delete()

        return Response(
            data={'message': 'Password reset successful!', 'ok': True},
            status=status.HTTP_200_OK
        )


class OTPReset(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=OTPResendSerializer,
        responses={
            201: openapi.Response(
                description='otp_key',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'otp_key': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='otp_key'
                        )
                    }
                )
            )
        }
    )
    def resend_otp(self, request):
        otp_key = request.data.get('otp_key')
        if not otp_key:
            return Response({'message': 'Pleas fill the blank!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        obj_otp = OTP.objects.filter(otp_key=otp_key).first()

        if obj_otp is None:
            return Response({'message': 'Otp_key is wrong!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        user = obj_otp.user
        if user and user.is_verified:
            return Response({'massage': 'User already verified!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        new_obj = OTP.objects.create(user=user)

        if check_otp(OTP.objects.filter(user=user)):
            return Response(
                data={'message': 'Too many attempts try after 12 hours', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_obj.save()
        send_otp(new_obj)
        return Response({'otp_key': new_obj.otp_key, 'ok': True}, status=status.HTTP_200_OK)
