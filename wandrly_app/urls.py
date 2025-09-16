from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_index, name='post-index'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/create', views.PostCreate.as_view(), name='post-create'),
]

