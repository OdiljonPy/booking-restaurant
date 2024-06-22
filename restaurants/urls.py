from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantCategoryActionViewSet, RestaurantViewSet, RoomTypeViewSet, \
    RestaurantRoomViewSet, \
    RestaurantRoomActionViewSet, RoomTypeActionViewSet, RestaurantMenuViewSet, RestaurantMenuActionsView, \
    ActionRestaurantViewSet, RestaurantFilterViewSet, CommentViewSet

urlpatterns = [
    path('filter/all/', RestaurantFilterViewSet.as_view({'get': 'show_restaurant'})),
    path('filter/', RestaurantFilterViewSet.as_view({'get': 'restaurant_filter_view'})),
    path('category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category', 'post': 'create_category'})),
    path('category/actions/<int:pk>',
         RestaurantCategoryActionViewSet.as_view(
             {'get': 'detail_category', 'patch': 'edit_category', 'delete': 'delete_category'})),
    path('add/', RestaurantViewSet.as_view({'post': 'add_restaurant'})),
    path('actions/<int:pk>/', ActionRestaurantViewSet.as_view({'get': 'show_restaurant_detail',
                                                               'patch': 'edit_restaurant',
                                                               'delete': 'delete_restaurant'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'show_room_type', 'post': 'add_room_type'})),
    path('room-type/actions/<int:pk>/',
         RoomTypeActionViewSet.as_view({'patch': 'edit_room_type', 'delete': 'delete_room_type'})),

    path('<int:pk>/room/', RestaurantRoomViewSet.as_view({'get': 'show_restaurant_room', 'post': 'add_room'})),
    path('actions/<int:pk>/room/', RestaurantRoomActionViewSet.as_view({'get': 'show_room_detail',
                                                                        'patch': 'edit_room',
                                                                        'delete': 'delete_room'})),

    path('menu/', RestaurantMenuViewSet.as_view({'get': 'show_restaurant_menu', 'post': 'add_restaurant_menu'})),
    path('actions/<int:pk>/menu/',
         RestaurantMenuActionsView.as_view({'get': 'show_menu_detail', 'patch': 'edit_menu', 'delete': 'delete_menu'})),

    path('comment/', CommentViewSet.as_view({'post': 'create'})),
    path('<int:restaurant_id>/comments/', CommentViewSet.as_view({'get': 'list'})),

]
