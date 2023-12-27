from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    verified = models.BooleanField(default=False)
    hsh = models.CharField(max_length=500)

# class Comment(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     body = models.TextField(max_length=120)
#     created = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey("Blog", on_delete=models.CASCADE)


class Blog(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField(max_length=300)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # comments = models.ManyToManyField(Comment, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
