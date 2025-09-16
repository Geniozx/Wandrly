from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

# Create your models here.
# class User(models.Model):
#     bio = models.TextField(max_length=250, blank=True)
#     profile_image = models.ImageField(uplaod_to="profiles/", blank=True, null=True)

#     def __str__(self):
#         return self.username



    
class Location(models.Model):
    continent = models.CharField(max_length=50)
    continent_code = models.CharField(max_length=5)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    coordinates = gis_models.PointField(geography=True, blank=True, null=True)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.continent})"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    media = models.ImageField(upload_to="posts/")
    caption = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="posts")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.caption[:2200]}"
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.id})
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:500]}"