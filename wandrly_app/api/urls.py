
from django.urls import path

from .views import (
    CurrentUserView,
    LoginView,
    LogoutView,
    RegisterView,
    csrf_token,
    health_check,
)

app_name = "api"

urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/csrf/", csrf_token, name="csrf"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="me"),
]
