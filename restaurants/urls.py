from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet, RoomTypeViewSet, \
    RestaurantRoomViewSet, RestaurantMenuViewSet, RestaurantFilterViewSet, CommentViewSet, MenuTypeViewSet

urlpatterns = [
    path('filter/all/', RestaurantFilterViewSet.as_view({'get': 'show_restaurant'})),
    path('filter/', RestaurantFilterViewSet.as_view({'get': 'restaurant_filter_view'})),

    path('category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category', 'post': 'create_category'})),
    path('category_edit/', RestaurantCategoryViewSet.as_view({'delete': 'delete_category'})),

    path('add/', RestaurantViewSet.as_view({'post': 'add_restaurant'})),
    path('edit/<int:pk>/', RestaurantViewSet.as_view({'get': 'show_restaurant_detail',
                                                      'patch': 'edit_restaurant',
                                                      'delete': 'delete_restaurant'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'show_room_type', 'post': 'add_room_type'})),
    path('room-type/<int:pk>/',
         RoomTypeViewSet.as_view({'patch': 'edit_room_type', 'delete': 'delete_room_type'})),

    path('room/', RestaurantRoomViewSet.as_view({'post': 'add_room'})),
    path('room/<int:pk>/',
         RestaurantRoomViewSet.as_view({'get': 'show_room_detail', 'patch': 'edit_room', 'delete': 'delete_room'})),

    path('menu_type/', MenuTypeViewSet.as_view({'post': 'add_menu_type', 'get': 'show_menu_type'})),
    path('menu_type/<int:pk>/', MenuTypeViewSet.as_view({'patch': 'edit_menu_type', 'delete': 'delete_menu_type'})),

    path('menu/', RestaurantMenuViewSet.as_view({'post': 'add_restaurant_menu'})),
    path('menu/<int:pk>/',
         RestaurantMenuViewSet.as_view({'get': 'show_menu_detail', 'patch': 'edit_menu', 'delete': 'delete_menu'})),

    path('comment/', CommentViewSet.as_view({'post': 'comment_create'})),
    path('comment/<int:pk>/', CommentViewSet.as_view({'get': 'comment_list'})),

]

# TODO: add roles for each view, need to fix validator for names, need to fix rating model, need to change comment model, need to write to representation for comments and categories to show it with restaurant, need to write paginator for comments and categories, add another things from real projects
