from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.views.generic import ListView
from django.views import View
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import UserForm, LoginForm, CheckoutForm, ReviewForm
from .models import Books, Cart, Checkout, Reviews, Wishlist

GENRE = [
    'Science Fiction',
    'Fantasy',
    'Mystery',
    'Thriller',
    'Romance',
    'Historical Fiction',
    'Non-Fiction',
    'Biography',
    'Self-Help',
    'Horror',
]

# Create your views here.

class UserRegister(View):
    def get(self, request):
        form = UserForm()
        return render(request, "form.html", {'form': form, 'request': request, 'genre':GENRE})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
        else:
            return render(request, "form.html", {'form': form, 'request': request, 'genre':GENRE})

##############################################################################################

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "form.html", {'form': form, 'request': request, 'genre':GENRE})
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")

        
        return render(request, "form.html", {'form': form, 'request': request, 'genre':GENRE})

##############################################################################################

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("home")

##############################################################################################

class BookDisplay(ListView):
    model = Books
    template_name = "home.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['request'] = self.request
        context['genre'] = GENRE
        if self.request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=self.request.user)
            
            if wishlist:
                wishlist = [x.book for x in wishlist]
                context['wishlist'] = wishlist
                
        else:
            context['wishlist'] = []

        all_books = context['books']

        rv_total = []
        len_rv = []

        for x in all_books:
            rv = Reviews.objects.filter(book=x)
            rvs = len(rv)
            total = 0
            len_rv.append(rvs)

            if rv:
                for rvw in rv:
                    total += rvw.rating
                rv_total.append(total/rvs)
            else:
                rv_total.append(total)
                len_rv.append(rvs)
        
        context['books_reviews'] = zip(all_books, rv_total, len_rv)

        return context

##############################################################################################

class CartDisplay(LoginRequiredMixin, View):
    model = Cart
    login_url = "/login/"

    def find_total(self, cart):
        total = 0
        for itm in cart:
            total += itm.book.price*itm.quantity
        return total

    def get(self, request):
        
        cart = self.model.objects.filter(user=request.user)
        total_orders = len(Checkout.objects.filter(user=request.user))

        if cart:
            total = self.find_total(cart)

            context = {'cart':cart, 'total': total, 'request': request, 'genre':GENRE}

            if total_orders >=5:
                context['disc'] = "You have received 25% discount"
                context['total'] = int(total*0.75)
            else:
                context['disc'] = "Order more than 5 items to receive 25% discount"
            

            return render(request, "cart.html", context)
        
        else:
            return HttpResponse("Cart is empty")
    
    def post(self, request):
        title = request.POST.get("title")
        author = request.POST.get("author")
        sign = request.POST.get('sign')
    
        book = Books.objects.get(title=title, author=author)

        total_orders = len(Checkout.objects.filter(user=request.user))
        
        cart = self.model.objects.filter(user=request.user, book=book)
        if sign:
            cart = cart[0]
            if sign == '+':
                cart.quantity += 1
                cart.save()
            
            else:
                qty = cart.quantity

                if qty == 1:
                    cart.delete()
                else:
                    cart.quantity -= 1
                    cart.save()
            
        elif cart:
            return redirect("cart")
        else:
            cart = self.model(user=request.user)
            cart.book = book
            cart.save()

        cart = self.model.objects.filter(user=request.user)
        total = self.find_total(cart)

        context = {'cart':cart, 'total': total, 'request': request, 'genre':GENRE}

        if total_orders >=5:
            context['disc'] = "You have received 25% discount"
            context['total'] = int(total*0.75)
        else:
            context['disc'] = "Order more than 5 items to receive 25% discount"
            

        return render(request, "cart.html", context)

##############################################################################################

class CheckoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        
        cart = Cart.objects.filter(user=request.user)
        if cart:
            form = CheckoutForm()
            return render(request, "form.html", {'form':form,'request': request, 'genre':GENRE})
        else:
            return HttpResponse("Cart is empty")
    
    def post(self, request):
        form = CheckoutForm(request.POST)

        if form.is_valid():
            cart = Cart.objects.filter(user=request.user)
            
            checkout = form.save(commit=False)

            for x in cart:
                checkout.user = x.user
                checkout.book = x.book
                checkout.quantity = x.quantity
                
                bk = Books.objects.get(title=x.book.title, author=x.book.author)

                bk.quantity -= x.quantity

                bk.save()

                print("Yes error")
                x.delete()
                checkout.save()
            
            return HttpResponse("Your order will be shipped within a minute")
        
        return render(request, "form.html", {'form':form, 'request':request, 'genre':GENRE})

##############################################################################################

class OrderHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = "order_history.html"
    context_object_name = "checkout"
    model = Checkout

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['request'] = self.request

        checkout = self.model.objects.filter(user=self.request.user)

        total = 0

        for usr in checkout:
            
            total += usr.book.price * usr.quantity

        context['total'] = total
        context['genre'] = GENRE
        context['checkout'] = checkout

        return context
        
##############################################################################################

class SearchView(View):
    model = Books

    def post(self, request):
        print(request.POST)
        itm = request.POST.get('search')

        books = self.model.objects.filter(
            Q(title__icontains=itm) | Q(author__icontains=itm) | Q(desc__icontains=itm)
        )
        
        context = {
            'books': books,
            'request': request,
            'genre': GENRE
        }

        return render(request, "home.html", context)

###################################################################################################
    
class FilterView(View):
    model = Books

    def post(self, request):
        itm = request.POST.get("genre")
        books = self.model.objects.filter(genre=itm)

        context = {
            'books': books,
            'request': request,
            'genre': GENRE
        }

        return render(request, "home.html", context)

######################################################################################
    
class WishlistView(View):
    model = Wishlist
    def get(self, request):
        wishlist = self.model.objects.filter(user=request.user)
        
        if wishlist:
            return render(request, "wishlist.html", {'wishlist': wishlist, 'request': request})
        else:
            return HttpResponse("Wishlist empty")
    
    def post(self, request):
        title = request.POST.get("title")
        author = request.POST.get("author")
        book = Books.objects.get(title=title, author=author)

        wishlist = self.model.objects.filter(user=request.user, book=book)
        
        if wishlist:
            wishlist.delete()
        else:
            wishlist = self.model(user=request.user, book=book)
            wishlist.save()
        
        wishlist = self.model.objects.filter(user=request.user)

        return render(request, "wishlist.html", {'wishlist': wishlist, 'request': request})

######################################################################################################
    
class ReviewView(View):
    model = Reviews

    def get(self, request, id):
        form = ReviewForm()
        book = get_object_or_404(Books, pk=id)
        reviews = Reviews.objects.filter(book=book)

        return render(request, "review.html", {'book': book, 'form': form, 'reviews':reviews})
    
    def post(self, request, id):
        form = ReviewForm(request.POST)

        if form.is_valid():
            book = get_object_or_404(Books, pk=id)

            if Reviews.objects.filter(user=request.user, book=book):
                return HttpResponse("You have already reviewed")
            
            frm = form.save(commit=False)
            frm.user = request.user
            frm.book = book
            frm.save()

        reviews = Reviews.objects.filter(book=book)

        return render(request, "review.html", {'book': book, 'form': ReviewForm(), 'reviews':reviews})
    
#########################################################################################################
    
class WishlistShareView(View):
    def get(self, request, id):
        usr = get_object_or_404(User, pk=id)
        wishlist = Wishlist.objects.filter(user=usr)

        return render(request, "wishlistshare.html", {'wishlist': wishlist, 'request': request})


    







            