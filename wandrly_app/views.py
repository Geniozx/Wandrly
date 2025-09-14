from django.shortcuts import render



# views.py

# Create your views here.
def home(request):
    return render(request, 'home.html')

def post_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})