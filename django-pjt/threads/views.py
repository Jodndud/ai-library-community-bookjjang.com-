
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

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

# 댓글 작성
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        thread_id = self.kwargs.get('pk')
        thread = generics.get_object_or_404(Thread, pk=thread_id)
        serializer.save(user=self.request.user, thread=thread)

# 좋아요 토글
class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thread = generics.get_object_or_404(Thread, pk=pk)
        user = request.user
        if user in thread.likes.all():
            thread.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            thread.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)
