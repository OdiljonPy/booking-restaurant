from django.urls import path
from .views import RestaurantViewSet, BookingViewSet, ManagementViewSet,  UserViewSet,BookingcostumerViewSet

urlpatterns = [
    path('users/<int:user_id>/', UserViewSet.as_view({'delete': 'delete_user'})),
    path('restaurants/', RestaurantViewSet.as_view({
        'get': 'list_restaurants',
    }), name='restaurant-list'),

    path('restaurants/<int:rest_id>/', RestaurantViewSet.as_view({
        'get': 'retrieve_restaurant', 'delete': 'delete_restaurant'
    }), name='restaurant-detail'),

    path('restaurants/<int:rest_id>/balance/', RestaurantViewSet.as_view({
        'get': 'restaurant_balance',
    }), name='restaurant-payment-balance'),

    path('restaurants/<int:rest_id>/statistics/', RestaurantViewSet.as_view({
        'get': 'restaurant_statistics',
    }), name='restaurant-statistics'),
    path('restaurants/<int:rest_id>/bookings/', BookingViewSet.as_view({
        'get': 'booking_list',
    }), name='restaurant-bookings'),

    path('restaurants/<int:rest_id>/bookings/<int:booking_id>/', BookingViewSet.as_view({
        'get': 'retrieve_booking', 'put': 'cancel_booking', 'delete': 'delete_booking'
    }), name='restaurant-bookings'),
    path('resturants/managers/',
         ManagementViewSet.as_view({'get': 'list_managers', 'post': 'create_manager'})),
    path('resturants/costumer_bookings/', BookingcostumerViewSet.as_view({'get': 'show_booking_costumer', 'post': 'create_booking_costumer'})),

]
