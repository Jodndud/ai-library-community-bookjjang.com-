# books/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.CharField(max_length=13)
    cover = models.URLField(null=True, blank=True)
    publisher = models.CharField(max_length=255)
    pub_date = models.DateField()
    author = models.CharField(max_length=255)  # <- 문자열임 (Author와 연결 안 됨)
    customer_review_rank = models.PositiveIntegerField()

    def __str__(self):
        return self.title



class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Book.author와 비교용
    bio = models.TextField(blank=True, null=True)         # Wikipedia로부터 가져온 소개
    photo = models.ImageField(upload_to='author_profiles/', blank=True, null=True)


    def __str__(self):
        return self.name

    # ✅ Book과의 연결 관계 (참조용 메서드)
    def books(self):
        return Book.objects.filter(author=self.name)
