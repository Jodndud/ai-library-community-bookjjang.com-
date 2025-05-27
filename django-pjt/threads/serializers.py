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
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    is_liked = serializers.SerializerMethodField()
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ['user', 'comments', 'like_count', 'cover_image']

    def validate_rating(self, value):
        allowed_values = [Decimal(f'{i / 2:.1f}') for i in range(11)]  # 0.0 ~ 5.0
        if value not in allowed_values:
            raise serializers.ValidationError("Rating must be between 0 and 5 in 0.5 increments.")
        return value

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj in user.liked_threads.all()
        return False
    