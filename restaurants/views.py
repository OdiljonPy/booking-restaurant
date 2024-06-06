from django.shortcuts import render


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu
from .serializers import CategorySerializer, RestaurantSerializer, RoomSerializer, RoomTypeSerializer, MenuSerializer


# RESTAURANT SECTION

def restaurant_filter_view(request):
    """
    Restaurant filtering view - bu yerda Restaurantlarni royxati kerak bolsa shu view ga murojat qilinadi.

    Diqqat: Ma'lum bir paremetrlar qabul qilinadi filterlash uchun, xech qanday parametr qabul qilinmasa toliq royxat
    pagination bilan qaytariladi.
    """

    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
        return Response(data={"List of restaurants": restaurant_serialize}, status=status.HTTP_200_OK)

#done
class RestaurantCategoryViewSet(ViewSet):
    def restaurant_category(self, request):
        category = RestaurantCategory.objects.all()
        category_serialize = CategorySerializer(category, many=True).data
        return Response(data={"list of categories": category_serialize}, status=status.HTTP_200_OK)

#done
class RestaurantViewSet(ViewSet):

    def add_restaurant(self, request):
        # author = request.user
        category = RestaurantCategory.objects.filter(id=request.data['category_id'])
        restaurant_obj = Restaurant.objects.create(restaurant_name=request.data['restaurant_name'],
                                                   picture=request.data['picture'],
                                                   description=request.data['description'],
                                                   address=request.data['address'], phone=request.data['phone'],
                                                   email=request.data['email'], service_fee=request.data['service_fee'],
                                                   category=category)
        restaurant_obj.save()
        return Response(data={'message': 'Restaurant successfully created'}, status=status.HTTP_201_CREATED)


class ActionRestaurantViewSet(ViewSet):
    def show_restaurant_detail(self, request, pk):
        restaurant_detail = Restaurant.objects.filter(id=pk).first()
        restaurant_serialize = RestaurantSerializer(restaurant_detail).data
        return Response(data={"restaurant_detail": restaurant_serialize}, status=status.HTTP_200_OK)

    #Need to fix.
    def edit_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
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




# ROOM SECTION.

class RoomTypeViewSet(ViewSet):
    def add_room_type(self, request):
        room_type = RoomType.objects.create(room_type=request.data['room_type'])
        room_type.save()
        return Response(data={"message": f"{room_type} type is created successfully"}, status=status.HTTP_201_CREATED)

    def show_room_type(request):
        room_type = RoomType.objects.all()
        room_type_serialize = RoomTypeSerializer(room_type, many=True).data
        return Response(data={"list of room types": room_type_serialize}, status=status.HTTP_200_OK)


class RoomTypeActionViewSet(ViewSet):
    #Need to fix
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


class RestaurantRoomViewSet(ViewSet):
=======
    pass


def restaturant_add_view(request):
    """
    Yangi restaurant qoshish uchun ishlatiladi.

    Talab qilinadi: Bunig uchun faqat Ma'lum toifadagi royxatdan otgan va shu api
    ga dostupi bor login qilgan user bolishi shart.
    """
    pass


def restaturant_actions_view(request):
    """
    Bu yerda restaurant ga tegishli amallarni request type ga qarab delete, get detail, edit, qilish amallarini bajarish
    uchun ishlatiladi.

    Diqqat: {id} - restaurant id sini parametr sifatida user tarafidan jonatilishi kerak.
    Talab qilinadi: Edit yoki delete qilish uchun user Super admin yoki, Restaurant egasi, Tzim manageri bolishi kerak
    """
    pass


# Room section

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


class RestaurantRoomActionViewSet(ViewSet):

    def show_room_detail(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk).first()
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"room_details": room_serialize}, status=status.HTTP_200_OK)


    #Need to fix.
    def edit_room(request, pk):
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

class RestaurantMenuViewSet(ViewSet):
    def show_restaurant_menu(self, request):
        menu = RestaurantMenu.objects.filter(restaurant_id=request.data['restaurant_id'])
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"menu": menu_serialize}, status=status.HTTP_200_OK)

    def add_restaurant_menu(self, request):
        menu = RestaurantMenu.objects.create(restaurant_id=request.data['restaurant_id'],
                                             name=request.data['name'],
                                             pictures=request.data['pictures'],
                                             price=request.data['price'],
                                             ingredients=request.data['ingredients'],
                                             description=request.dadta['description'],
                                             )
        menu.save()
        message = f"{menu.name} is created successfully"
        return Response(data={"message": message}, status=status.HTTP_201_CREATED)


class RestaurantMenuActionsView(ViewSet):
    def show_menu_detail(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"menu_details": menu_serialize}, status=status.HTTP_200_OK)

    #Need to fix.
    def edit_menu(request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        menu['name'] = request.data['name']
        menu['price'] = request.data['price']
        ...
        menu.save(update_fields=['name', 'price'])
        menu_serialize = MenuSerializer(menu).data
        message = f"{menu.name} is changed"
        return Response(data={"message": message}, status=status.HTTP_200_OK)

    def delete_menu(request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        message = f"{menu.name} is deleted"
        del menu
        return Response(data={"message": message}, status=status.HTTP_200_OK)



# Comments and Reviews

def restaurant_comment_view(request):
    pass


def restaurant_rate_view(request):
    pass
