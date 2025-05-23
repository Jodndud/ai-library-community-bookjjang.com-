from django.urls import path
from .views import (
    ThreadListCreateView, ThreadDetailView,
    CommentCreateView, ToggleLikeView
)

urlpatterns = [
    path('', ThreadListCreateView.as_view(), name='thread-list'),
    path('<int:pk>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('<int:pk>/comments/', CommentCreateView.as_view(), name='thread-comment'),
    path('<int:pk>/like/', ToggleLikeView.as_view(), name='thread-like'),
]
