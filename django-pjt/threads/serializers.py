# threads/serializers.py
from rest_framework import serializers
from decimal import Decimal
from .models import Thread, Comment

class CommentSerializer(serializers.ModelSerializer):
    # user는 username 등으로만 출력 (읽기 전용)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    # user는 username 등으로만 출력 (읽기 전용)
    user = serializers.StringRelatedField(read_only=True)
    # 댓글 목록 (읽기 전용)
    comments = CommentSerializer(many=True, read_only=True)
    # 좋아요 개수 (읽기 전용)
    likes_count = serializers.SerializerMethodField()
    # cover_image는 업로드 및 검증이 필요한 필드
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Thread
        fields = '__all__'  # 모든 필드 사용
    
    def validate_rating(self, value):
        if value not in [Decimal(x) for x in [f'{i/2:.1f}' for i in range(0, 11)]]:
            raise serializers.ValidationError("Rating must be between 0 and 5 in 0.5 increments.")
        return value
    
    def get_likes_count(self, obj):
        # 좋아요 개수 반환
        return obj.likes.count()

    