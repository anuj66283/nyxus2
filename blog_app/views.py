from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from datetime import datetime


# Create your views here.
def list_post(request):
    blogs = Post.objects.all()
    return render(request, 'post_list.html', {'blogs': blogs})

def detail_post(request, id):
    blog = get_object_or_404(Post.objects.prefetch_related('comments'), pk=id)
    return render(request, 'post_detail.html', {'blog': blog})

def form_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            
            form.instance.published_date = datetime.now().date()

            form.save()

            return redirect('list_post')

    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})
