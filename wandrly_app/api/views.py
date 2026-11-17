from django.middleware.csrf import get_token
from django.contrib.auth import login, logout, get_user_model
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from wandrly_app.models import Profile

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    ProfileDetailSerializer,
    ProfileUpdateSerializer,
    PublicProfileSerializer,
)

from .privacy import (
    can_view_profile_content,
    users_are_blocked,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "service": "roamly-api",
            "version": "v1",
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    token = get_token(request)

    return Response({
        "csrfToken": token,
    })



@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        login(request, user)

        return Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        return Response({
            "user": UserSerializer(user).data,
        })



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response({
            "detail": "Successfully logged out."
        })


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({
            "user": serializer.data
        })



User = get_user_model()


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(
            Profile.objects.select_related("user"),
            user=request.user,
        )

        serializer = ProfileDetailSerializer(
            profile,
            context={"request": request},
        )

        return Response(serializer.data)

    def patch(self, request):
        profile = get_object_or_404(
            Profile,
            user=request.user,
        )

        serializer = ProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            ProfileDetailSerializer(
                profile,
                context={"request": request},
            ).data
        )


class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        target_user = get_object_or_404(
            User,
            username=username,
        )

        if users_are_blocked(request.user, target_user):
            return Response(
                {"detail": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        profile = get_object_or_404(
            Profile.objects.select_related("user"),
            user=target_user,
        )

        if can_view_profile_content(request.user, profile):
            serializer = ProfileDetailSerializer(
                profile,
                context={"request": request},
            )
        else:
            serializer = PublicProfileSerializer(
                profile,
                context={"request": request},
            )

        return Response(serializer.data)
