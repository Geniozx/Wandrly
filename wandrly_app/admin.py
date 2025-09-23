from django.contrib import admin
from .models import Post, Comment, Profile, Location


# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Comment)