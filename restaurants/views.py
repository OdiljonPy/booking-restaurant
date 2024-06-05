from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom
from .serializers import CategorySerializer, RestaurantSerializer, RoomSerializer, RoomTypeSerializer


# Restaurant Section

def restaurant_filter_view(request):
    """
    Restaurant filtering view - bu yerda Restaurantlarni royxati kerak bolsa shu view ga murojat qilinadi.

    Diqqat: Ma'lum bir paremetrlar qabul qilinadi filterlash uchun, xech qanday parametr qabul qilinmasa toliq royxat
    pagination bilan qaytariladi.
    """
    pass


class RestaurantCategoryViewSet(ViewSet):
    def restaurant_category(self, request):
        category = RestaurantCategory.objects.all()
        category_serialize = CategorySerializer(category, many=True).data
        return Response(data={"list of categories": category_serialize}, status=status.HTTP_200_OK)


class RestaurantViewSet(ViewSet):
    def add_restaurant(self, request):
        restaurant_obj = Restaurant.objects.create(restaurant_name=request.data['restaurant_name'],
                                                   picture=request.data['picture'],
                                                   description=request.data['description'],
                                                   address=request.data['address'], phone=request.data['phone'],
                                                   email=request.data['email'], service_fee=request.data['service_fee'])
        restaurant_obj.save()
        return Response(data={'message': 'Restaurant successfully created'}, status=status.HTTP_201_CREATED)

    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
        return Response(data={"List of restaurants": restaurant_serialize}, status=status.HTTP_200_OK)


class ActionRestaurantViewSet(ViewSet):
    # Bu view quydagi 3 funksiyani ishlatish uchun foydalanishga moljalangan edi.
    #
    def show_restaurant_detail(self, request, pk):
        restaurant_detail = Restaurant.objects.filter(id=pk).first()
        restaurant_serialize = RestaurantSerializer(restaurant_detail).data
        return Response(data={"restaurant_detail": restaurant_serialize}, status=status.HTTP_200_OK)

    def edit_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
        # Update ni to'g'rilab yozib chiqishimiz kerak
        restaurant['restaurant_name'] = request.data['restaurant_name']
        restaurant['picture'] = request.data['picture']
        ...
        restaurant.save(update_fields=['restaurant_name', 'picture'])
        restaurant_serialize = RestaurantSerializer(restaurant).data
        return Response(data={"message": f"Information of {restaurant_serialize}  were changed"},
                        status=status.HTTP_200_OK)

    def delete_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
        message = f"{restaurant.restaurant_name} was deleted"
        del restaurant
        return Response(data={"message": message}, status=status.HTTP_200_OK)


# Room section

def RoomTypeViewSet(request):
    def add_room_type(self, request):
        room_type = RoomType.objects.create(room_type=request.data['room_type'])
        room_type.save()
        return Response(data={"message": f"{room_type} type is created successfully"}, status=status.HTTP_201_CREATED)

    def show_room_type(request):
        room_type = RoomType.objects.all()
        room_type_serialize = RoomTypeSerializer(room_type, many=True).data
        return Response(data={"list of room types": room_type_serialize}, status=status.HTTP_200_OK)


def RoomTypeActionViewSet(request):
    def edit_room_type(request, pk):
        room_type = RoomType.objects.filter(id=pk).first()
        room_type['room_type'] = request.data['room_type']
        room_type.save(update_fields=['room_type'])
        message = f"{room_type} type was updated"
        return Response(data={"message": message}, status=status.HTTP_200_OK)

    def delete_room_type(request, pk):
        room_type = RoomType.objects.filter(id=pk).first()
        message = f"{room_type} type was deleted"
        del room_type
        return Response(data={"message": message}, status=status.HTTP_200_OK)


def RestaurantRoomViewSet(ViewSet):
    """
    Restaurantlarni room lari ni royxat korinishda olish uchun

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinmaydi: User ixtiyoriy bolishi kerak, royxatdan otgan otmagan, admin admin emas ...
    """

    def add_room(self, request):
        room = RestaurantRoom.objects.create(
            restaurant=Restaurant.objects.filter(id=request.data['restaurant_id']).first(),

            room_name=request.data['room_name'],
            pictures=request.data['pictures'],
            description=request.data['description'],
            people_number=request.data['people_number'],
            waiters_number=request.data['waiters_number'],
            room_type=RoomType.objects.filter(id=request.data['room_type_id']).first(), )
        room.save()
        return Response(data={"message": f"{room} room is created successfully"}, status=status.HTTP_201_CREATED)

    def show_restaurant_room(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk)
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"list of rooms": room_serialize}, status=status.HTTP_200_OK)


def RestaurantRoomActionView(request):
    """
    Restaurant uchun yangi room qoshish uchun ishlatiladi.

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinadi: User restaurant egasi, yoki tizim adminstratori bolishi kerak
    """

    def edit_room_room(request, pk):
        room = RestaurantRoom.objects.filter(id=pk).first()
        room['room_name'] = request.data['room_name']
        room['pictures'] = request.data['pictures']
        room['description'] = request.data['description']
        ...
        room.save(update_fields=['room_name', 'pictures', 'description'])
        room_serialize = RoomSerializer(room).data
        return Response(data={"message": f"Information of {room_serialize} were changed"}, status=status.HTTP_200_OK)

    def delete_room(request, pk):
        room = RestaurantRoom.objects.filter(id=pk).first()
        message = f"{room} was deleted"
        del room
        return Response(data={"message": message}, status=status.HTTP_200_OK)


# Menu section

def restaurant_menu_view(request):
    pass


def restaurant_menu_add_view(request):
    pass


def restaurant_menu_actions_view(request):
    pass


# Comments and Reviews

def restaurant_comment_view(request):
    pass


def restaurant_rate_view(request):
    pass
