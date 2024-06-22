from django.urls import path
from .views import TelegramUserViewSet, RestaurantViewSet, RoomsViewSet, RestMenuViewSet

urlpatterns = [
    path('user/add/', TelegramUserViewSet.as_view({'post': 'create'})),

    path('rest/all/', RestaurantViewSet.as_view({'get': 'all_restaurant'})),
    path('rest/categories/', RestaurantViewSet.as_view({'get': 'category_restaurant'})),

    path('rest/room/type/', RoomsViewSet.as_view({'get': 'room_type'})),
    path('rest/rooms/', RoomsViewSet.as_view({'get': 'restaurant_room'})),

    path('rest/menu/type/', RestMenuViewSet.as_view({'get': 'menu_type'})),
    path('rest/menu/', RestMenuViewSet.as_view({'get': 'restaurant_menu'})),
]
