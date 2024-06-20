from django.urls import path
from .views import TelegramUserViewSet

urlpatterns = [
    path('telegram/send/', TelegramUserViewSet.as_view({'post': 'create'}))
]
