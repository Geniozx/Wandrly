from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models




    
class Location(models.Model):
    continent = models.CharField(max_length=50)
    continent_code = models.CharField(max_length=5)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)

    coordinates = gis_models.PointField(geography=True, blank=True, null=True)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.continent})"

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
        return {self.name}