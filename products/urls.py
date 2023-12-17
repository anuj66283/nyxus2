from django.urls import path
from .views import register, single, prdts

urlpatterns = [
    path("register/", register, name='register'),
    path("product/<int:id>/", single, name='single'),
    path("products/", prdts, name="products")
] 

