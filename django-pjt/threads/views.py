# threads/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer
from books.utils.create_ai_image import generate_cover_image  # 추가

# 전체 글 목록 조회 및 글 작성
# URL: /api/v1/threads/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def thread_list_create(request, book_pk):
    if request.method == 'GET':
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            # Thread 인스턴스 우선 생성
            thread = serializer.save(user=request.user, book_id=book_pk)
            
            # 게시글 내용 전체를 AI에 전달 (title, content, emotion_text)
            emotion_text = request.data.get('emotion_text', '')
            ai_prompt = f"{thread.title}\n{thread.content}\n{emotion_text}"
            cover_img = generate_cover_image(thread.book, ai_prompt)
            if cover_img:
                thread.cover_image = cover_img
                thread.save()

            # 새로 저장된 thread를 다시 직렬화하여 반환
            return Response(ThreadSerializer(thread).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 단일 글 조회
# URL: /api/v1/threads/<int:pk>/
@api_view(['GET'])
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)

# 댓글 조회 및 작성
# URL: /api/v1/threads/<int:pk>/comments/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, book_pk, pk):
    thread = get_object_or_404(Thread, pk=pk, book_id=book_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(thread=thread).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 좋아요 토글
# URL: /api/v1/threads/<int:pk>/like/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user
    if user in thread.likes.all():
        thread.likes.remove(user)
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        thread.likes.add(user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
