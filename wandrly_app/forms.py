from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post, Location

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name") or ""
        user.last_name = self.cleaned_data.get("last_name") or ""
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]


class PostForm(forms.ModelForm):
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = ['media', 'caption']

    def save(self, commit=True, user=None):
        loc = Location.objects.create(
            city=self.cleaned_data.get('city', ''),
            country=self.cleaned_data.get('country', ''),
            coordinates=f"POINT({self.cleaned_data['longitude']} {self.cleaned_data['latitude']})"
        )
        post = super().save(commit=False)
        post.user = user
        post.location = loc
        if commit:
            post.save()
        return post