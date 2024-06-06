from django.urls import path
from .views import UserCreateAPIView, auth_me, OTPViewSet

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('login/', auth_me),

    path('otp/send/', OTPViewSet.as_view({'post': 'send'})),
    path('otp/verify/', OTPViewSet.as_view({'post': 'verify'})),
]