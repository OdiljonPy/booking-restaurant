from django.urls import path
from .views import UserViewSet, OtpViewSet, ChangePasswordViewSet, ResetPassword

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),

    path('verify/', OtpViewSet.as_view({'post': 'verify'}), name='verify'),
    path('password/update/', ChangePasswordViewSet.as_view({'put': 'update'})),

    path('password/reset/', ResetPassword.as_view({'post': 'reset'})),
    path('password/verify/', ResetPassword.as_view({'post': 'verify'})),
    path('password/reset_new/', ResetPassword.as_view({'post': 'reset_new'})),
]
