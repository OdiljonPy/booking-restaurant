from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet, RoomTypeViewSet, \
    RestaurantRoomViewSet, RestaurantMenuViewSet, RestaurantFilterViewSet, CommentViewSet, MenuTypeViewSet

urlpatterns = [
    path('filter/all/', RestaurantFilterViewSet.as_view({'get': 'show_restaurant'})),
    path('filter/', RestaurantFilterViewSet.as_view({'get': 'restaurant_filter_view'})),
    path('category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category', 'post': 'create_category'})),
    path('category/actions/<int:pk>',
         RestaurantCategoryViewSet.as_view(
             {'patch': 'edit_category', 'delete': 'delete_category'})),
    path('add/', RestaurantViewSet.as_view({'post': 'add_restaurant'})),
    path('add/<int:pk>/', RestaurantViewSet.as_view({'get': 'show_restaurant_detail',
                                                     'patch': 'edit_restaurant',
                                                     'delete': 'delete_restaurant'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'show_room_type', 'post': 'add_room_type'})),
    path('room-type/<int:pk>/',
         RoomTypeViewSet.as_view({'patch': 'edit_room_type', 'delete': 'delete_room_type'})),

    path('<int:pk>/room/', RestaurantRoomViewSet.as_view(
        {'get': 'show_room_detail', 'post': 'add_room', 'patch': 'edit_room', 'delete': 'delete_room'})),

    path('menu_type/', MenuTypeViewSet.as_view({'post': 'add_menu_type', 'get': 'show_menu_type'})),
    path('<int:pk>/menu_type/', MenuTypeViewSet.as_view({'patch': 'edit_menu_type', 'delete': 'delete_menu_type'})),

    path('menu/', RestaurantMenuViewSet.as_view({'post': 'add_restaurant_menu'})),
    path('<int:pk>/menu/',
         RestaurantMenuViewSet.as_view({'get': 'show_menu_detail', 'patch': 'edit_menu', 'delete': 'delete_menu'})),

    path('comment/', CommentViewSet.as_view({'post': 'comment_create'})),
    path('<int:pk>/comment/', CommentViewSet.as_view({'get': 'comment_list'})),

]