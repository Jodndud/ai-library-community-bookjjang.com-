from django.urls import path
from . import views

urlpatterns = [
    # 책 목록 조회 API
    path('', views.BookListView.as_view(), name='book_list_api'),

    # 책 상세 정보 조회 API
    path('<int:pk>/', views.BookDetailAPIView.as_view(), name='book_detail_api'),
]
