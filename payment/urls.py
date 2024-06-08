from django.urls import path
from .views import OTPViewSet, PaymentViewSet

urlpatterns = [
    path('card/otp/send/', OTPViewSet.as_view({'post': 'send'})),
    path('card/otp/verify/', OTPViewSet.as_view({'post': 'verify'})),
    path('pay/', PaymentViewSet.as_view({'post': 'pay'})),
]