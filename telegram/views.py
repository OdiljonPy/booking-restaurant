from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from .serializer import TelegramUserSerializer, RestSerializer, ResCategorySerializer, RestaurantRoomSerializer, \
    RoomsTypeSerializer, MenuTypesSerializer, RestaurantMenuSerializer
from .utils import telegram_add
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, MenuType


class TelegramUserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Telegram User',
        request_body=TelegramUserSerializer,
        responses={200: "User successfully created",
                   400: TelegramUserSerializer},

    )
    def create(self, request):
        data = request.data
        phone = TelegramUser.objects.filter(phone=data['phone']).first()
        user = TelegramUser.objects.filter(telegram_id=data['telegram_id']).first()
        if user is None:
            if phone is None:
                serializer = TelegramUserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    obj = TelegramUser.objects.create(telegram_id=data['telegram_id'], first_name=data['first_name'],
                                                      last_name=data['last_name'], phone=data['phone'],
                                                      username=data['username'])
                    obj.save()
                    telegram_add(obj)
                    return Response('User created', status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"message": "This phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)


class RestaurantViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='See Restaurant details',
        request_body=RestSerializer,
    )
    def all_restaurant(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestSerializer(restaurants, many=True).data
        return Response(data={'Restaurants': serializer}, status=status.HTTP_200_OK)

    def category_restaurant(self, request):  # pan-asian, europe, usa, arabic, turkish, family
        category = RestaurantCategory.objects.all()
        serializer = ResCategorySerializer(category, many=True).data
        return Response(data={'Categories': serializer}, status=status.HTTP_200_OK)


class RoomsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='See Romms details',
        request_body=RestaurantRoomSerializer,
    )
    def room_type(self, request):  # luxe, family, primary,
        rooms_type = RoomType.objects.all()
        serializer = RoomsTypeSerializer(rooms_type, many=True).data
        return Response(data={'Room Types': serializer}, status=status.HTTP_200_OK)

    def restaurant_room(self, request):
        restaurant_room = RestaurantRoom.objects.all()
        serializer = RestaurantRoomSerializer(restaurant_room, many=True).data
        return Response(data={'Restaurant Rooms': serializer}, status=status.HTTP_200_OK)


class RestMenuViewSet(ViewSet):  # RESTAURANT MENU
    @swagger_auto_schema(
        operation_description='See Restaurant Menu details',
        request_body=RestaurantMenuSerializer,
    )
    def menu_filter(self, request, pk):
        menu = RestaurantMenu.objects.filter(restaurant_id=pk).order_by('restaurant__name')
        serializer = RestaurantMenuSerializer(menu, many=True).data
        return Response(data={'Restaurant Menu': serializer}, status=status.HTTP_200_OK)

    def menu_type(self, request):
        menu_type = MenuType.objects.all()
        serializer = MenuTypesSerializer(menu_type, many=True).data
        return Response(data={'Menu Types': serializer}, status=status.HTTP_200_OK)

    def restaurant_menu(self, request):
        restaurant_menu = RestaurantMenu.objects.all()
        serializer = RestaurantMenuSerializer(restaurant_menu, many=True).data
        return Response(data={'Restaurant Menu': serializer}, status=status.HTTP_200_OK)
