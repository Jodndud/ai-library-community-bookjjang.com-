import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .utils.wiki_api import get_wikipedia_content, get_wikipedia_image
# 책 목록 조회 API
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# 책 상세 정보 조회 API
class BookDetailAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)

class AuthorInfoByBookAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        author_name = book.author

        author_obj, created = Author.objects.get_or_create(name=author_name)

        if created or not author_obj.bio or not author_obj.photo:
            # Wikipedia 요약 및 이미지 URL 가져오기
            wiki_data = get_wikipedia_content(author_name)
            if wiki_data:
                author_obj.bio = wiki_data.get("summary", "")

            img_url = get_wikipedia_image(author_name)
            if img_url:
                response_img = requests.get(img_url)
                if response_img.status_code == 200:
                    from django.core.files.base import ContentFile
                    import os
                    filename = os.path.basename(img_url)
                    author_obj.photo.save(filename, ContentFile(response_img.content), save=False)

            author_obj.save()

        serializer = AuthorSerializer(author_obj, context={'request': request})
        return Response(serializer.data)
