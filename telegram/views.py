from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from .serializer import TelegramUserSerializer, TGRestaurantSerializer, TGRestaurantMenuSerializer, \
    TGRoomTypeSerializer
from .utils import telegram_add
from .models import TelegramUser
from restaurants.models import Restaurant, RoomType, RestaurantMenu


class TelegramUserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Telegram User',
        request_body=TelegramUserSerializer,
        responses={200: "User successfully created",
                   400: TelegramUserSerializer},

    )
    def create(self, request):
        data = request.data
        user = TelegramUser.objects.filter(user_id=data.get('user_id')).first()
        if not user:
            serializer = TelegramUserSerializer(data=data)
            if serializer.is_valid():
                obj = serializer.save()
                telegram_add(obj)
                return Response('User created', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)


class RestaurantViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='See Restaurant details',
    )
    def all_restaurant(self, request):
        restaurants = Restaurant.objects.all()
        serializer = TGRestaurantSerializer(restaurants, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def restaurant_category_detail(self, request, pk):  # pan-asian, europe, arabic, turkish, family
        category = Restaurant.objects.filter(category_id=pk)
        serializer = TGRestaurantSerializer(category, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def filter_restaurant_menu_types(self, request, pk):
        menu_type = Restaurant.objects.filter(restaurantmenu__menu_type_id=pk)
        serializer = TGRestaurantSerializer(menu_type, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)


class RoomsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='See Romms details',
    )
    def restaurant_room_type(self, request, pk):  # luxe, family, primary,
        rooms_type = RoomType.objects.filter(restaurantroom__restaurant_id=pk)
        serializer = TGRoomTypeSerializer(rooms_type, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)


class RestMenuViewSet(ViewSet):  # RESTAURANT MENU
    @swagger_auto_schema(
        operation_description='See Restaurant Menu details',
    )
    def restaurant_menu(self, request, pk):
        restaurant_menu = RestaurantMenu.objects.filter(restaurant_id=pk)
        serializer = TGRestaurantMenuSerializer(restaurant_menu, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)
