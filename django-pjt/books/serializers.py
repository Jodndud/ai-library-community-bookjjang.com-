from rest_framework import serializers
from .models import Book, Author
from threads.models import Thread  # Thread에서 rating을 가져옴
from django.db.models import Avg  # 평균 계산용

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'  # Book 모델의 모든 필드를 직렬화
    
    def get_average_rating(self, obj):
        avg = obj.threads.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg is not None else None


class BookDetailSerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_threads(self, obj):
        from threads.serializers import ThreadSerializer  # ✅ 지연 import로 해결
        threads = obj.threads.all()
        return ThreadSerializer(threads, many=True, context=self.context).data


class AuthorSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['name', 'bio', 'photo']

    def get_photo(self, obj):
        request = self.context.get('request', None)
        if request and obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        elif obj.photo and hasattr(obj.photo, 'url'):
            return obj.photo.url  # fallback: 절대 경로는 아니지만 최소 url 제공
        return None