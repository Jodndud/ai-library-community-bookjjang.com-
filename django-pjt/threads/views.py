from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

# 전체 + 작성
class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 단일 조회
class ThreadDetailView(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

# 댓글 작성 + 조회 통합
class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 댓글 목록 조회
    def get(self, request, pk):
        comments = Comment.objects.filter(thread_id=pk).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 댓글 작성
    def post(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 좋아요 토글
class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        user = request.user
        if user in thread.likes.all():
            thread.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            thread.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)
