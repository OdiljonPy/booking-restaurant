from django.urls import path
from .views import RestaurantViewSet, BookingViewSet, ManagementViewSet, EmployerViewSet

urlpatterns = [
    path('restaurants/', RestaurantViewSet.as_view({
        'get': 'list',
    }), name='restaurant-list'),

    path('restaurants/<int:rest_id>/', RestaurantViewSet.as_view({
        'get': 'retrieve',
    }), name='restaurant-detail'),

    path('restaurants/<int:rest_id>/balance/', RestaurantViewSet.as_view({
        'get': 'balance',
    }), name='restaurant-payment-balance'),

    path('restaurants/<int:rest_id>/statistics/', RestaurantViewSet.as_view({
        'get': 'statistics',
    }), name='restaurant-statistics'),
    path('restaurants/<int:rest_id>/bookings/', BookingViewSet.as_view({
        'get': 'list',
    }), name='restaurant-bookings'),

    path('restaurants/<int:rest_id>/bookings/<int:booking_id>/', BookingViewSet.as_view({
        'get': 'retrieve', 'delete': 'cancel',
    }), name='restaurant-bookings'),
    path('resturants/<int:rest_id>/managers/', ManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('resturants/<int:rest_id>/managers/employers/', EmployerViewSet.as_view({'get': 'list', 'post': 'create'})),
]
