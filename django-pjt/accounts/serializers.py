from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import User

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    age = serializers.IntegerField(required=False)
    yearly_reading_amount = serializers.IntegerField(required=False)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    favorite_genres = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['age'] = self.validated_data.get('age', None)
        data['yearly_reading_amount'] = self.validated_data.get('yearly_reading_amount', None)
        data['profile_image'] = self.validated_data.get('profile_image', None)
        data['favorite_genres'] = self.validated_data.get('favorite_genres', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.age = self.validated_data.get('age', None)
        user.yearly_reading_amount = self.validated_data.get('yearly_reading_amount', None)
        user.profile_image = self.validated_data.get('profile_image', None)
        user.favorite_genres = self.validated_data.get('favorite_genres', '')
        user.save()
        return user
    
    # 닉네임 중복 체크 확인
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value