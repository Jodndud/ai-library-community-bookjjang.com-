from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book  # books 앱의 모델 가져오기
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Thread(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='threads')  # 책과 연결
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=255)
    content = models.TextField()
    # ⭐ 0 ~ 5 점, 0.5 단위 별점
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('5.0'))
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_users', blank=True)  # 좋아요 기능
    # ✅ 좋아요 수 저장
    like_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='thread_covers/', blank=True, null=True)  # 서버에 저장
    def __str__(self):
        return f'{self.title} - {self.user.username}'
    
class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.thread.title}'