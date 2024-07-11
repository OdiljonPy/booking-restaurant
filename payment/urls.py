from django.urls import path
from .views import PaymentViewSet

urlpatterns = [
    path('pay/', PaymentViewSet.as_view({'post': 'receive_money'})),
    path('pay-back/', PaymentViewSet.as_view({'post': 'return_money'}))
]