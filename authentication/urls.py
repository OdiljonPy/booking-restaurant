from django.urls import path
from .views import UserViewSet, ChangePasswordViewSet, ResetPassword, OTPReset

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('verify/', UserViewSet.as_view({'post': 'verify'}), name='verify'),

    path('password/update/', ChangePasswordViewSet.as_view({'put': 'update'})),

    path('password/otp/resend/', ResetPassword.as_view({'post': 'reset'})),
    path('password/otp/verify/', ResetPassword.as_view({'post': 'verify'})),
    path('password/token/reset/', ResetPassword.as_view({'post': 'reset_new'})),

    path('resend_otp/', OTPReset.as_view({'post': 'resend_otp'})),

]
