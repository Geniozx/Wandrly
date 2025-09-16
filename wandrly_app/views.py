from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CommentForm

def home(request):
    return render(request, 'home.html')

def post_index(request):
    posts = []   #Post.objects.all().order_by('created_at')
    comment_form = CommentForm
    return render(request, 'posts/index.html', {'posts': posts, 'comment_form': comment_form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm
    return render(request, 'posts/detail.html', {'post': post, 'comment_form': comment_form})

class PostCreate(CreateView):
    model = Post
    fields = '__all__'

class PostUpdate(UpdateView):
    model = Post
    fields = '__all__'

class PostDelete(DeleteView):
    model = Post
    success_url = '/posts/'


