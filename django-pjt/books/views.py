import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, BookDetailSerializer
from .utils.wiki_api import process_author_info_by_book_pk
from rest_framework.permissions import AllowAny

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

## 책 기반 작가 정보 조회
# URL: api/v1/books/<int:pk>/author/
@api_view(['GET'])
@permission_classes([AllowAny])
def author_info_by_book(request, pk):
    """
    book pk를 받아서 위키피디아+GPT 기반으로 작가 정보(소개, 대표작, 사진 등) 반환
    """
    try:
        author_data = process_author_info_by_book_pk(pk)
        if author_data is None:
            return Response(
                {"detail": "책 또는 작가 정보를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(author_data)

    except Exception as e:
        print("[ERROR] author_info_by_book 실패:", e)
        return Response(
            {"detail": "작가 정보를 처리하는 도중 오류가 발생했습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
