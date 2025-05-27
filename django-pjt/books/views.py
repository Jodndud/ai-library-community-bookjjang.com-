import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, BookDetailSerializer
from .utils.wiki_api import process_author_info_by_book_pk

# 책 목록 조회
# URL: api/v1/books/
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# 책 상세 조회
# URL: api/v1/books/<int:pk>/
@api_view(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book, context={'request': request})
    return Response(serializer.data)

# 책 기반 작가 정보 조회
# URL: api/v1/books/<int:pk>/author/
@api_view(['GET'])
def author_info_by_book(request, pk):
    """
    book pk를 받아서 위키피디아+GPT 기반으로 작가 정보(소개, 대표작, 사진 등) 반환
    """
    # DB에서 Book 존재 확인 및 작가 정보 처리 함수 호출
    author_data = process_author_info_by_book_pk(pk)
    if author_data is None:
        return Response({"detail": "책 또는 작가 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    # author_data 예시 키:
    # {
    #   "author_name": "홍길동",
    #   "author_info": "홍길동은 ...",
    #   "author_works": "대표작1, 대표작2, 대표작3",
    #   "author_photo_url": "/media/author_profiles/author_10_홍길동.jpg",
    #   "wiki_url": "https://ko.wikipedia.org/wiki/홍길동_(작가)"
    # }

    return Response(author_data)
