from django.urls import path
from .views import PaymentViewSet

urlpatterns = [
    path('payment-data/', PaymentViewSet.as_view({'post': 'post'})),
]