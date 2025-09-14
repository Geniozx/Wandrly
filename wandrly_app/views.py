from django.shortcuts import render



# views.py

class Post:
    def __init__(self, media, caption, location, likes, createdAt, comments):
        self.media = media
        self.caption = caption
        self.location = location
        self.likes = likes
        self.createdAt = createdAt
        self.comments = comments

# Create a list of Cat instances
posts = [
    Post('image', 'I Went Somewhere', 'New York', 'Likes', '2 seconds ago', 'that is awesome'),
]



# Create your views here.
def home(request):
    return render(request, 'home.html')

def post_index(request):
    return render(request, 'posts/index.html', {'posts': posts})