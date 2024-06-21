from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),

]