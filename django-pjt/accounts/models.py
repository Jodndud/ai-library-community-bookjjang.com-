
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, blank=False, null=False) # unique : 중복허용하지 않는다.
    age = models.PositiveIntegerField(null=True, blank=True)
    yearly_reading_amount = models.PositiveIntegerField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    favorite_genres = models.CharField(
        max_length=100,
        blank=True,
        help_text="여러 장르는 쉼표(,)로 구분해 주세요. 예: 소설, 에세이, SF"
    )

    @property
    def favorite_genres_list(self):
        if not self.favorite_genres:
            return []
        return [genre.strip() for genre in self.favorite_genres.split(',')]


