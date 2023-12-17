from django.urls import path
from .views import list_post, detail_post, form_post

urlpatterns = [
    path("blogs", list_post, name="list_post"),
    path("blog/<int:id>/", detail_post, name="detail_post"),
    path("form_post/", form_post, name="form_post")
]