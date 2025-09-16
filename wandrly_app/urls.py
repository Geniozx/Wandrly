from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_index, name='post-index'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/create', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
]

