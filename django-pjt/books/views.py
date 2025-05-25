import os
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .utils.wiki_api import process_wikipedia_info, generate_author_gpt_info


# 책 목록 조회 API
class BookListView(APIView):
    def get(self, request):
        # 모든 책을 가져옴
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# 책 상세 정보 조회 API
class BookDetailAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class AuthorInfoByBookAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        author_name = book.author

        author_obj, created = Author.objects.get_or_create(name=author_name)

        if created or not author_obj.bio or not author_obj.photo:
            wiki_summary, image_path = process_wikipedia_info(book)
            author_info, author_works = generate_author_gpt_info(book, wiki_summary)

            author_obj.bio = author_info

            if image_path:
                abs_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
                if os.path.exists(abs_image_path):
                    with open(abs_image_path, 'rb') as img_file:
                        file_name = os.path.basename(image_path)
                        author_obj.photo.save(file_name, File(img_file), save=False)

            author_obj.save()

            book.author_info = author_info
            book.author_works = author_works
            book.save()

        serializer = AuthorSerializer(author_obj, context={'request': request})
        return Response(serializer.data)
