from django.shortcuts import render



# views.py

# Create your views here.
def home(request):
    return render(request, 'home.html')

def post_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def post_detail(request, post_id):
    posts = Post.objects.get(id=post_id)
    return render(request, 'posts/detail.html', {'post': post})
