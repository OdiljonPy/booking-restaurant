from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from .models import Restaurant, RestaurantCategory
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, RestaurantSerializer


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
                                                   picture=request.data['picture'], description=request.data['description'],
                                                   address=request.data['address'], phone=request.data['phone'],
                                                   email=request.data['email'], service_fee=request.data['service_fee'])
        restaurant_obj.save()
        return Response(data={'message': 'Restaurant successfully created'}, status=status.HTTP_201_CREATED)

    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
        return Response(data={"List of restaurants": restaurant_serialize}, status=status.HTTP_200_OK)



class ActionRestaurantViewSet(ViewSet):
    def show_restaurant(self, request, pk):
        pass



# Room section


def restaurant_room_view(request):
    """
    Restaurantlarni room lari ni royxat korinishda olish uchun

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinmaydi: User ixtiyoriy bolishi kerak, royxatdan otgan otmagan, admin admin emas ...
    """

    pass


def restaurant_room_add_view(request):
    """
    Restaurant uchun yangi room qoshish uchun ishlatiladi.

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinadi: User restaurant egasi, yoki tizim adminstratori bolishi kerak
    """
    pass


def restaurant_room_actions_view(request):
    pass


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
