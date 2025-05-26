from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book  # books 앱의 모델 가져오기

User = get_user_model()

class Thread(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='threads')  # 책과 연결
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_threads', blank=True)  # 좋아요 기능

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