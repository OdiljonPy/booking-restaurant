from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet, RoomTypeViewSet, RestaurantRoomViewSet, \
    RestaurantRoomActionViewSet, RoomTypeActionViewSet, RestaurantMenuViewSet, RestaurantMenuActionsView

urlpatterns = [
    # Abbos shu yerdagi restaurantlarni olib tashlash kerak:
    # <sabab>bu yerga restaurant/ bilan keladi restaurant/add/restaurant/ xolatga kelib qoladi</sabab>

    # path('add/restaurant/', RestaurantViewSet.as_view({'post': 'add_restaurant', 'get': 'show_restaurant'})),
    # path('add/restaurant/category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),

    path('restaurant-category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),
    path('add/', RestaurantViewSet.as_view({'post': 'add_restaurant'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'restaurant_room'})),
    path('room-type/actions', RoomTypeActionViewSet.as_view({'post': 'edit_room_type', 'delete': 'delete_room_type'})),

    path('rooms/', RestaurantRoomViewSet.as_view({'get': 'restaurant_room'})),
    path('rooms/actions/',
         RoomTypeActionViewSet.as_view({'get': 'show_room_detail', 'post': 'edit_room', 'delete': 'delete_room'})),

    path('menu/', RestaurantMenuViewSet.as_view({'get': 'show_restaurant_menu', 'post': 'add_restaurant_menu'})),
    path('menu/actions/',
         RestaurantRoomActionViewSet.as_view({'get': 'show_menu_detail', 'post': 'edit_menu', 'delete': 'delete_menu'}))

]
