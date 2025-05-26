# books/urls.py
from django.urls import path#,include
from . import views as book_views
from threads import views as thread_views

urlpatterns = [
    # 도서 관련
    path('', book_views.book_list, name='book-list'),                                # GET /api/v1/books/
    path('<int:pk>/', book_views.book_detail, name='book-detail'),                   # GET /api/v1/books/<int:pk>/
    path('<int:pk>/author/', book_views.author_info_by_book, name='author-info'),    # GET /api/v1/books/<int:pk>/author/

    # 쓰레드 관련 (책 별로)
    path('threads/', thread_views.thread_list, name='thread-list'),  # GET
    path('<int:book_pk>/threads/', thread_views.thread_list_create, name='thread-list-create'),  # GET, POST
    path('<int:book_pk>/threads/<int:pk>/', thread_views.thread_detail, name='thread-detail'),    # GET 상세
    path('<int:book_pk>/threads/<int:pk>/comments/', thread_views.comment_list_create, name='comment-list-create'),  # GET, POST
   
    #쓰레드 관련 (책 관계없이 전체)
    path('threads/', thread_views.thread_list, name='thread-list'),  # GET /api/v1/books/threads/
    path('threads/<int:pk>/like/', thread_views.toggle_like, name='thread-like'),  # POST
]
