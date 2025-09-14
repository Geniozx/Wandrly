from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# class User(AbstractUser):
#     bio = models.TextField(max_length=250, blank=True)
#     profile_image = models.ImageField(uplaod_to="profiles/", blank=True, null=True)

#     def __str__(self):
#         return self.username


class Post(models.Model):
    # user = models.ForeignKey(User, on_delte=CASCADE, related_name="posts")
    media = models.ImageField(upload_to="posts/")
    caption = models.TextField(blank=True)
    # location = models.ForeignKey(
    #     Location, on_delete=models.SET_NULL, null=True, related_names="posts"
    # )
    # likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.caption[:2200]}"
    
class Location(models.Model):
    continent = models.CharField(max_length=50)
    continent_code = models.CharField(max_length=5)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        parts = [self.city, self.state, self.coutry, self.continent]
        return ", ".join([p for p in parts if p])