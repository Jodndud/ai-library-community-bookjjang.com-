from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer
from books.utils.create_ai_image import generate_cover_image  # 추가

# ✅ 전체 글 목록 조회 (책과 무관)
# URL: /api/v1/books/threads/
@api_view(['GET'])
def thread_list(request):
    threads = Thread.objects.all()
    serializer = ThreadSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)

# ✅ 책 별 글 목록 조회 및 글 작성
# URL: /api/v1/books/<int:book_pk>/threads/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def thread_list_create(request, book_pk):
    if request.method == 'GET':
        threads = Thread.objects.filter(book_id=book_pk)
        serializer = ThreadSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # ✅ 인증 체크 명시적으로 수행
        if not request.user or not request.user.is_authenticated:
            return Response({'detail': '인증이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ThreadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            thread = serializer.save(user=request.user, book_id=book_pk)

            # AI 커버 이미지 생성
            emotion_text = request.data.get('emotion_text', '')
            ai_prompt = f"{thread.title}\n{thread.content}\n{emotion_text}"
            cover_img = generate_cover_image(thread.book, ai_prompt)
            if cover_img:
                thread.cover_image = cover_img
                thread.save()

            return Response(ThreadSerializer(thread, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 단일 글 조회
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/
@api_view(['GET'])
def thread_detail(request, book_pk, pk):
    thread = get_object_or_404(Thread, pk=pk, book_id=book_pk)
    serializer = ThreadSerializer(thread, context={'request': request})  # context 추가
    return Response(serializer.data)


# ✅ 댓글 조회 및 작성
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/comments/

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, book_pk, pk):
    thread = get_object_or_404(Thread, pk=pk, book_id=book_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(thread=thread).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})  # context 추가해도 무방
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 좋아요 토글
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/like/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, book_pk, pk):  # ← book_pk 인자 추가
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user
    
    if thread in user.liked_threads.all():
        user.liked_threads.remove(thread)
        thread.like_count = thread.liked_by_users.count()
        thread.save()
        return Response({
            'status': 'unliked',
            'like_count': thread.like_count,
            'user_liked_threads': list(user.liked_threads.values_list('id', flat=True))
        }, status=status.HTTP_200_OK)
    else:
        user.liked_threads.add(thread)
        thread.like_count = thread.liked_by_users.count()
        thread.save()
        return Response({
            'status': 'liked',
            'like_count': thread.like_count,
            'user_liked_threads': list(user.liked_threads.values_list('id', flat=True))
        }, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_threads_list(request):
    user = request.user
    threads = Thread.objects.filter(likes=user)
    serializer = ThreadSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)
   
# ✅ 단일 글 조회
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/
@api_view(['GET'])
def thread_detail(request, book_pk, pk):
    thread = get_object_or_404(Thread, pk=pk, book_id=book_pk)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)


# ✅ 댓글 조회 및 작성
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/comments/
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

# ✅ 좋아요 토글
# URL: /api/v1/books/<int:book_pk>/threads/<int:pk>/like/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, book_pk, pk):  # ← book_pk 인자 추가
    thread = get_object_or_404(Thread, pk=pk, book_id=book_pk)
    user = request.user
    
    if thread.likes.filter(id=user.id).exists():
        thread.likes.remove(user)
        thread.like_count = thread.likes.count()
        thread.save()
        return Response({
            'status': 'unliked',
            'like_count': thread.like_count,
            'likes': [u.username for u in thread.likes.all()]
        }, status=status.HTTP_200_OK)
    else:
        thread.likes.add(user)
        thread.like_count = thread.likes.count()
        thread.save()
        return Response({
            'status': 'liked',
            'like_count': thread.like_count,
            'likes': [u.username for u in thread.likes.all()]
        }, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_threads_list(request):
    user = request.user
    threads = Thread.objects.filter(likes=user)
    serializer = ThreadSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)
   