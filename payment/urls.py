from django.urls import path
from .views import PaymentViewSet

urlpatterns = [
    path('info/', PaymentViewSet.as_view({'post': 'info'})),
]