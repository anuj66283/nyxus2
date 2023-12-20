from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_all, name="view_all"),
    path("update/<int:id>/", views.update_blog, name="update_blog"),
    path("blog/<int:id>/", views.view_blog, name="view_blog"),
    path("delete/<int:id>/", views.delete_blog, name="delete_blog"),
    path("create/", views.create_blog, name="create_blog"),
    path("accounts/signup/", views.signup, name='signup'),
    path("accounts/login/", views.signin, name='signin'),
    path("accounts/logout/", views.signout, name='signout'),

]
