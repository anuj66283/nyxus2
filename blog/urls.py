from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogView.as_view(), name="view_all"),
    path("create/", views.CreateBlog.as_view(), name="create"),
    path("delete/<int:pk>/", views.DeleteBlog.as_view(), name="delete"),
    path("blog/<int:pk>/", views.SingleBlogView.as_view(), name="blog"),
    path("update/<int:pk>/", views.UpdateBlog.as_view(), name="update"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("verify/<str:hsh>", views.OTP.as_view(), name="otp"),
    path("logout/", views.UserLogout.as_view(), name="logout")
]
