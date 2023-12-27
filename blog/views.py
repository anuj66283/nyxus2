import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from django.core.mail import send_mail

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView
)
from django.views import View

from django.contrib.auth import authenticate, login, logout

from .models import CustomUser, Blog
from .forms import UserForm, BlogForm, LoginForm


import hashlib

def create_hash(val):
    hash_object = hashlib.sha256()
    hash_object.update(val.encode('utf-8'))
    return hash_object.hexdigest()[:100]

class UserRegister(View):
    def get(self, request):
        form = UserForm()
        return render(request, "register.html", {'form': form})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            hsh = create_hash(username+email)

            form.instance.hsh = hsh

            form.save()

            otp = reverse("otp", kwargs={'hsh': hsh})

            return redirect(otp)
        
        else:
            return render(request, "register.html", {'form': form})

class UserLogin(View):

    model = CustomUser

    def get(self, request):
        return render(request, "login.html", {'form':LoginForm()})
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get("password")


            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("view_all")

        return render(request, "login.html", {'form': form})

class OTP(View):
    def get(self, request, hsh):
        user = CustomUser.objects.get(hsh=hsh)
        if user:
            if user.verified == True:
                return HttpResponse("Already verified")
            else:
                
                random.seed(user.id*54)
                x = random.randint(1000, 10000)

                send_mail("YOur otp", str(x), from_email="test@test.com", recipient_list=[user.email])
                return render(request, "otp.html")
        return HttpResponse("Invalid access")

        
    def post(self, request, hsh):
        otp = request.POST.get("otp")
        user = CustomUser.objects.get(hsh=hsh)

        random.seed(user.id*54)
        x = random.randint(1000, 10000)
        if x == int(otp):
            user.verified = True
            user.save()
            return redirect("login")
        
        return HttpResponse("Invalid otp")

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("view_all")

####################################################################SW


class BlogView(ListView):
    model = Blog
    template_name = "view_all.html"
    context_object_name = "blogs"

class SingleBlogView(DetailView):
    model = Blog
    template_name = "view_single.html"
    context_object_name = "blog"

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "create_blog.html"
    success_url = "/"
    login_url = "/login/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateBlog(LoginRequiredMixin,  UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "update_blog.html"
    success_url = "/"
    login_url = "/login/"

    def test_func(self):
        return self.request.user == self.get_object().author

class DeleteBlog(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = "delete_blog.html"
    context_object_name = "blog"
    success_url = "/"
    login_url = "/login/"

    def test_func(self):
        return self.request.user == self.get_object().author

