from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    price = models.IntegerField()
    # uri = models.URLField(default='')

    uri = models.FileField(upload_to="books/")
    GENRE = [
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Historical Fiction', 'Historical Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Biography', 'Biography'),
        ('Self-Help', 'Self-Help'),
        ('Horror', 'Horror'),
    ]
    genre = models.CharField(max_length=60, choices=GENRE)
    desc = models.TextField()
    quantity = models.IntegerField(default=100)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 11)])  
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)