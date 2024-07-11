from django.urls import path
from .views import TelegramUserViewSet, RestaurantViewSet, RoomsViewSet, RestMenuViewSet

urlpatterns = [
    path('user/', TelegramUserViewSet.as_view({'post': 'create'})),

    path('restaurant/', RestaurantViewSet.as_view({'get': 'all_restaurant'})),
    path('restaurant/categories/<int:pk>', RestaurantViewSet.as_view({'get': 'restaurant_category_detail'})),
    path('restaurant/filter/<int:pk>', RestaurantViewSet.as_view({'get': 'filter_restaurant_menu_types'})),

    path('restaurant/room/type/<int:pk>', RoomsViewSet.as_view({'get': 'restaurant_room_type'})),

    path('restaurant/menu/<int:pk>', RestMenuViewSet.as_view({'get': 'restaurant_menu'})),
]
