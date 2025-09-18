from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('posts/', views.post_index, name='post-index'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('posts/<int:post_id>/add-comment/', views.add_comment, name='add-comment'),
]

