from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import UserSarializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


class UserRegisterAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSarializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


