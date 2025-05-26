from django.urls import path
from .views import (
    ThreadListCreateView, ThreadDetailView,
    CommentListCreateView, ToggleLikeView
)

urlpatterns = [
    path('', ThreadListCreateView.as_view(), name='thread-list'),
    path('<int:pk>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('<int:pk>/comments/', CommentListCreateView.as_view(), name='thread-comments'),
    path('<int:pk>/like/', ToggleLikeView.as_view(), name='thread-like'),
]
