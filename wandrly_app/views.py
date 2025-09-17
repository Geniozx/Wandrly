from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CommentForm

def home(request):
    return render(request, 'home.html')

def post_index(request):
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm
    coords = [
        {
            "lat": p.location.coordinates.y,
            "lng": p.location.coordinates.x,
            "caption": p.caption,
            "city": p.location.city,
            "country": p.location.country,
            "id": p.id
        }
        for p in posts if p.location and p.location.coordinates
    ]
    return render(request, 'posts/index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'coords': coords
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm
    coords = None
    if post.location and post.location.coordinates:
        coords = {
            "lat": post.location.coordinates.y,
            "lng": post.location.coordinates.x,
        }
    return render(request, 'posts/detail.html', {
        'post': post,
        'comment_form': comment_form,
        'coords': coords
    })

def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.save()
    return redirect('post-detail', post_id=post_id)

class PostCreate(CreateView):
    model = Post
    fields = '__all__'

class PostUpdate(UpdateView):
    model = Post
    fields = '__all__'

class PostDelete(DeleteView):
    model = Post
    success_url = '/posts/'





