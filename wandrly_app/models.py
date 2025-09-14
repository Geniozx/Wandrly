from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delte=CASCADE, related_name="posts")
    media = models.ImageField(upload_to="posts/")
    caption = models.TextField(max_length=2200, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_names="posts"
    )
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

