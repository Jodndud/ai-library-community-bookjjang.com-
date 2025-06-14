"""
URL configuration for finalpjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# finalpjt/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 로그인/로그아웃
    path('accounts/', include('dj_rest_auth.urls')),  # login/logout 등 기본 제공

    # 회원가입
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),

    # 마이페이지 (accounts/mypage/)
    path('accounts/', include('accounts.urls')),

    # 도서 API
    path('api/v1/books/', include('books.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

