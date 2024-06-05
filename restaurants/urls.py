from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet, RoomTypeViewSet, RestaurantRoomViewSet

urlpatterns = [
    # Abbos shu yerdagi restaurantlarni olib tashlash kerak:
    # <sabab>bu yerga restaurant/ bilan keladi restaurant/add/restaurant/ xolatga kelib qoladi</sabab>
    path('restaurant-category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),
    path('/', RestaurantViewSet.as_view({'post': 'add_restaurant', 'get': 'show_restaurant'})),

    # path('add/restaurant/', RestaurantViewSet.as_view({'post': 'add_restaurant', 'get': 'show_restaurant'})),
    # path('add/restaurant/category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),

    path('room-type/', RoomTypeViewSet.as_view({'get': 'restaurant_room'})),
    path('rooms/', RestaurantRoomViewSet.as_view({'get': 'restaurant_room'})),
    # path('action/restaurant/<int:pk>', )
]
