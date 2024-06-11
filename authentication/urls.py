from django.urls import path
from .views import UserViewSet, OtpViewSet, ChangeViewSet
urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('verify/', OtpViewSet.as_view({'post': 'verify'}), name='verify'),

    path('change/', ChangeViewSet.as_view({'post': 'change'}), name='change'),
    # path('change_password/', change_password, name='change_password'),
]