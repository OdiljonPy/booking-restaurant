from django.urls import path
from .views import RestaurantCategoryViewSet, RestaurantViewSet

urlpatterns = [
    path('add/restaurant/', RestaurantViewSet.as_view({'post': 'add_restaurant', 'get': 'show_restaurant'})),
    path('add/restaurant/category/', RestaurantCategoryViewSet.as_view({'get': 'restaurant_category'})),
    # path('action/restaurant/<int:pk>', )
]