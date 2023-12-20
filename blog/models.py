from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField(max_length=300)
    author = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

