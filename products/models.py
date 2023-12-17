from django.db import models
import os

# dir = os.path.join("media", "images")

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="images")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)