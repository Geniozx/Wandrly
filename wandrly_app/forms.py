from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post, Location
from django.contrib.gis.geos import Point

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
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ['media', 'caption']

    def save(self, commit=True, user=None, instance=None):
        post = instance or super().save(commit=False)


        post.caption = self.cleaned_data.get('caption', post.caption)
        media = self.cleaned_data.get('media')
        if media:
            post.media = media

        if user:
            post.user = user

        # Handle location
        city = self.cleaned_data.get('city') or ''
        country = self.cleaned_data.get('country') or ''
        lat = self.cleaned_data.get('latitude')
        lng = self.cleaned_data.get('longitude')
        coordinates = Point(lng, lat) if lat is not None and lng is not None else None

        if post.location:
            loc = post.location
            loc.city = city or loc.city
            loc.country = country or loc.country or 'Unknown'
            if coordinates:
                loc.coordinates = coordinates
            loc.save()
        elif city or country or coordinates:
            loc = Location.objects.create(
                city=city or '',
                country=country or 'Unknown',
                coordinates=coordinates
            )
            post.location = loc

        if commit:
            post.save()
        return post