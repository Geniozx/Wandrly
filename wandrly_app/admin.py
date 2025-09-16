from django.contrib import admin
from .models import Post, Location, Comment


# Register your models here.
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Comment)