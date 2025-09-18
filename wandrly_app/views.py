from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Profile
from .forms import CommentForm, UserCreationForm, UserForm, ProfileForm, PostForm


def home(request):
    posts = Post.objects.all().order_by("-created_at")

    coords = []
    for p in posts:
        if p.location and p.location.coordinates:
            coords.append({
                "lat": p.location.coordinates.y,
                "lng": p.location.coordinates.x,
                "caption": p.caption,
                "city": p.location.city,
                "country": p.location.country,
                "id": p.id,
            })

    return render(request, "home.html", {
        "coords": coords,
        "user_authenticated": request.user.is_authenticated
    })

@login_required(login_url="login")
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

@login_required(login_url="login")
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

@login_required(login_url="login")
def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user = request.user
        new_comment.save()
    return redirect('post-detail', post_id=post_id)

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'wandrly_app/post_form.html'

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect('post-index')


class PostUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Post
    fields = ['media', 'caption', 'location']


class PostDelete(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Post
    success_url = '/posts/'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                bio=form.cleaned_data.get("bio", "")
            )
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, "profile_edit.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })




