from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    price = models.IntegerField()
    genre = models.CharField(max_length=60)
    desc = models.TextField()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Books)

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Books)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)