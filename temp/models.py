from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=40)
    bio = models.TextField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=20)

class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    published_date = models.DateField()