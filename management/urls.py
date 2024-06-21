from django.urls import path
from .views import RestaurantViewSet, ManagementViewSet,EmployerViewset

urlpatterns = [
    path('restaurants/', RestaurantViewSet.as_view({
        'get': 'list',
    }), name='restaurant-list'),

    path('restaurants/<int:pk>/', RestaurantViewSet.as_view({
        'get': 'retrieve',
    }), name='restaurant-detail'),

    path('restaurants/<int:pk>/bookings/', RestaurantViewSet.as_view({
        'get': 'booking',
    }), name='restaurant-bookings'),

    path('restaurants/<int:pk>/cancel-booking/', RestaurantViewSet.as_view({
        'delete': 'cancel_booking',
    }), name='restaurant-cancel-booking'),

    path('restaurants/<int:pk>/payment-balance/', RestaurantViewSet.as_view({
        'get': 'payment_balance',
    }), name='restaurant-payment-balance'),

    path('restaurants/<int:pk>/statistics/', RestaurantViewSet.as_view({
        'get': 'statistics',
    }), name='restaurant-statistics'),
    path('resturant/manager/', ManagementViewSet.as_view({'get': 'show_mangers', 'post': 'create_manager'})),
    path('resturant/employer/', EmployerViewset.as_view({'get': 'show_employer', 'post': 'create_employer'})),
]
