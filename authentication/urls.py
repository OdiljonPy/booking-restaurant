from django.urls import path
from .views import UserViewSet, OtpViewSet, ChangePasswordViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('verify/', OtpViewSet.as_view({'post': 'verify'}), name='verify'),
    path('password/update/', ChangePasswordViewSet.as_view({'put': 'update'})),

]
