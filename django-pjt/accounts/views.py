from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from threads.serializers import ThreadSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    user = request.user
    liked_threads = user.liked_threads.all()
    liked_threads_serialized = ThreadSerializer(liked_threads, many=True, context={'request': request}).data

    user_data = {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'email': user.email,
        'age': user.age,
        'yearly_reading_amount': user.yearly_reading_amount,
        'profile_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
        'favorite_genres': user.favorite_genres_list,
        'liked_threads': liked_threads_serialized,
    }
    return Response(user_data)