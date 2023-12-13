from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=40)
    bio = models.TextField(verbose_name="Enter bio")

class Book(models.Model):
    title = models.CharField(max_length=40)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()

