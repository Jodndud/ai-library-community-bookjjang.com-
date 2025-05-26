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

class AuthorSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['name', 'bio', 'photo']

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        return None