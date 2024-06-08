from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet, RoomTypeViewSet, RestaurantRoomViewSet, \
    RestaurantRoomActionViewSet, RoomTypeActionViewSet, RestaurantMenuViewSet, RestaurantMenuActionsView, \
    ActionRestaurantViewSet, RestaurantFilterViewSet

urlpatterns = [
    path('filter/', RestaurantFilterViewSet.as_view({'get': 'show_restaurant'})),
    path('filter/<str:pk>/', RestaurantFilterViewSet.as_view({'get': 'restaurant_filter_view'})),
    path('category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),
    path('add/', RestaurantViewSet.as_view({'post': 'add_restaurant'})),
    path('actions/<int:pk>/', ActionRestaurantViewSet.as_view({'get': 'show_restaurant_detail',
                                                               'patch': 'edit_restaurant',
                                                               'delete': 'delete_restaurant'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'show_room_type', 'post': 'add_room_type'})),
    path('room-type/actions/<int:pk>/',
         RoomTypeActionViewSet.as_view({'patch': 'edit_room_type', 'delete': 'delete_room_type'})),

    path('rooms/', RestaurantRoomViewSet.as_view({'get': 'show_restaurant_room', 'post': 'add_room'})),
    path('rooms/actions/', RestaurantRoomActionViewSet.as_view({'get': 'show_room_detail',
                                                                'patch': 'edit_room',
                                                                'delete': 'delete_room'})),

    path('menu/', RestaurantMenuViewSet.as_view({'get': 'show_restaurant_menu', 'post': 'add_restaurant_menu'})),
    path('menu/actions/',
         RestaurantMenuActionsView.as_view({'get': 'show_menu_detail', 'patch': 'edit_menu', 'delete': 'delete_menu'}))

]
