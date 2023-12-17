from django.db import models

# Create your models here.

class Comments(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=100)
    author = models.CharField(max_length=30)
    published_date = models.DateField()
    cmnts = models.ManyToManyField(Comments, related_name='cmnts', blank=True)

