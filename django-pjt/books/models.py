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
    author = models.CharField(max_length=255)
    customer_review_rank = models.PositiveIntegerField()

    def __str__(self):
        return self.title
