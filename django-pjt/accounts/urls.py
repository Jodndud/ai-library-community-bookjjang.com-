from django.urls import path
from .views import mypage

urlpatterns = [
    path('mypage/', mypage, name='mypage'),  # /accounts/mypage/ 경로
]