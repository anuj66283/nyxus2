from django.urls import path
from . import views

    #path("product/<int:id>/", single, name='single'),

urlpatterns = [
    path("create-product/", views.create_products, name='create_products'),
    path("read-products/", views.read_products, name="read_products"),
    path("update-product/<int:id>/", views.update_product, name="update_product"),
    path("delete-product/<int:id>", views.delete_product, name="delete_product"),

    path("create-category/", views.create_category, name='create_category'),
    path("read-category/", views.read_category, name="read_category"),
    path("update-category/<int:id>/", views.update_category, name="update_category"),
    path("delete-category/<int:id>", views.delete_category, name="delete_category"),
] 

