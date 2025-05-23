from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

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
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=404)
