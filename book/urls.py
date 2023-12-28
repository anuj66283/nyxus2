from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.UserLogin.as_view(), name="login"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("home/", views.BookDisplay.as_view(), name="home"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("cart/", views.CartDisplay.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("history/", views.OrderHistoryView.as_view(), name="history"),
    path("search/", views.SearchView.as_view(), name="search"),
]