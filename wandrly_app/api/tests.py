from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.test import APIClient

from wandrly_app.models import Follow, FollowRequest, UserBlock

User = get_user_model()


class HealthEndpointTests(TestCase):
    def test_health_endpoint_returns_expected_response(self):
        response = self.client.get(reverse("api:health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "roamly-api",
                "version": "v1",
            },
        )

    def test_health_endpoint_allows_anonymous_access(self):
        client = APIClient()

        response = client.get(reverse("api:health"))

        self.assertEqual(response.status_code, 200)


class DefaultAPIPermissionTests(TestCase):
    def test_default_permission_requires_authentication(self):
        @api_view(["GET"])
        def protected_view(request):
            return Response({"message": "protected"})

        from django.test import RequestFactory

        request = RequestFactory().get("/api/v1/protected-test/")
        response = protected_view(request)

        self.assertEqual(response.status_code, 403)


class CSRFEndpointTests(TestCase):
    def test_csrf_endpoint_returns_token(self):
        response = self.client.get(reverse("api:csrf"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfToken", response.json())
        self.assertTrue(response.json()["csrfToken"])

    def test_csrf_endpoint_sets_httponly_cookie(self):
        client = Client(enforce_csrf_checks=True)

        response = client.get(reverse("api:csrf"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)

        csrf_cookie = response.cookies[settings.CSRF_COOKIE_NAME]

        self.assertTrue(csrf_cookie["httponly"])
        self.assertEqual(csrf_cookie["samesite"], "Lax")

    def test_csrf_endpoint_allows_anonymous_users(self):
        response = Client().get(reverse("api:csrf"))

        self.assertEqual(response.status_code, 200)



class AuthenticationEndpointTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def get_csrf_token(self):
        response = self.client.get(reverse("api:csrf"))
        return response.json()["csrfToken"]

    def test_registration_requires_csrf(self):
        response = self.client.post(
            reverse("api:register"),
            data={
                "username": "traveler",
                "email": "traveler@example.com",
                "password": "SecureTravelPass123!",
                "password_confirm": "SecureTravelPass123!",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_registration_creates_user(self):
        token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:register"),
            data={
                "username": "traveler",
                "email": "traveler@example.com",
                "password": "SecureTravelPass123!",
                "password_confirm": "SecureTravelPass123!",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="traveler").exists()
        )
        self.assertNotIn("password", response.json()["user"])

    def test_login_requires_csrf(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        response = self.client.post(
            reverse("api:login"),
            data={
                "username": "traveler",
                "password": "SecureTravelPass123!",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_login_accepts_valid_credentials(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:login"),
            data={
                "username": "traveler",
                "password": "SecureTravelPass123!",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["user"]["username"],
            "traveler",
        )

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:login"),
            data={
                "username": "traveler",
                "password": "IncorrectPassword",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 400)


    def test_current_user_requires_authentication(self):
        response = self.client.get(reverse("api:me"))

        self.assertEqual(response.status_code, 403)

    def test_current_user_returns_authenticated_user(self):
        user = User.objects.create_user(
            username="traveler",
            email="traveler@example.com",
            password="SecureTravelPass123!",
        )

        self.client.force_login(user)

        response = self.client.get(reverse("api:me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["id"], user.id)
        self.assertEqual(
            response.json()["user"]["username"],
            "traveler",
        )
        self.assertNotIn("password", response.json()["user"])

    def test_logout_requires_authentication(self):
        response = self.client.post(reverse("api:logout"))

        self.assertEqual(response.status_code, 403)

    def test_logout_requires_csrf(self):
        user = User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        self.client.force_login(user)

        response = self.client.post(reverse("api:logout"))

        self.assertEqual(response.status_code, 403)

    def test_logout_ends_authenticated_session(self):
        user = User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        self.client.force_login(user)

        token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:logout"),
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        me_response = self.client.get(reverse("api:me"))

        self.assertEqual(me_response.status_code, 403)



    def post_with_csrf(self, url_name, payload):
        token = self.get_csrf_token()

        return self.client.post(
            reverse(url_name),
            data=payload,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

    def test_registration_rejects_mismatched_passwords(self):
        response = self.post_with_csrf(
            "api:register",
            {
                "username": "traveler",
                "email": "traveler@example.com",
                "password": "SecureTravelPass123!",
                "password_confirm": "DifferentTravelPass123!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            User.objects.filter(username="traveler").exists()
        )

    def test_registration_rejects_weak_password(self):
        response = self.post_with_csrf(
            "api:register",
            {
                "username": "traveler",
                "email": "traveler@example.com",
                "password": "123",
                "password_confirm": "123",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            User.objects.filter(username="traveler").exists()
        )

    def test_registration_rejects_duplicate_username(self):
        User.objects.create_user(
            username="traveler",
            email="original@example.com",
            password="SecureTravelPass123!",
        )

        response = self.post_with_csrf(
            "api:register",
            {
                "username": "traveler",
                "email": "new@example.com",
                "password": "AnotherSecurePass123!",
                "password_confirm": "AnotherSecurePass123!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            User.objects.filter(username="traveler").count(),
            1,
        )

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing",
            email="traveler@example.com",
            password="SecureTravelPass123!",
        )

        response = self.post_with_csrf(
            "api:register",
            {
                "username": "newtraveler",
                "email": "traveler@example.com",
                "password": "AnotherSecurePass123!",
                "password_confirm": "AnotherSecurePass123!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            User.objects.filter(username="newtraveler").exists()
        )

    def test_registration_creates_authenticated_session(self):
        response = self.post_with_csrf(
            "api:register",
            {
                "username": "traveler",
                "email": "traveler@example.com",
                "password": "SecureTravelPass123!",
                "password_confirm": "SecureTravelPass123!",
            },
        )

        self.assertEqual(response.status_code, 201)

        me_response = self.client.get(reverse("api:me"))

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(
            me_response.json()["user"]["username"],
            "traveler",
        )

    def test_login_creates_persistent_session(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        response = self.post_with_csrf(
            "api:login",
            {
                "username": "traveler",
                "password": "SecureTravelPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)

        me_response = self.client.get(reverse("api:me"))

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(
            me_response.json()["user"]["username"],
            "traveler",
        )

    def test_login_rotates_csrf_token(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        old_token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:login"),
            data={
                "username": "traveler",
                "password": "SecureTravelPass123!",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=old_token,
        )

        self.assertEqual(response.status_code, 200)

        new_token = self.get_csrf_token()

        self.assertNotEqual(old_token, new_token)

    def test_old_csrf_token_rejected_after_login(self):
        User.objects.create_user(
            username="traveler",
            password="SecureTravelPass123!",
        )

        old_token = self.get_csrf_token()

        response = self.client.post(
            reverse("api:login"),
            data={
                "username": "traveler",
                "password": "SecureTravelPass123!",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=old_token,
        )

        self.assertEqual(response.status_code, 200)

        logout_response = self.client.post(
            reverse("api:logout"),
            HTTP_X_CSRFTOKEN=old_token,
        )

        self.assertEqual(logout_response.status_code, 403)



class ProfileEndpointTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

        self.owner = User.objects.create_user(
            username="traveler",
            email="traveler@example.com",
            password="SecureTravelPass123!",
        )

        self.viewer = User.objects.create_user(
            username="explorer",
            email="explorer@example.com",
            password="SecureTravelPass123!",
        )

        self.owner.profile.display_name = "Travel Explorer"
        self.owner.profile.bio = "Exploring the world."
        self.owner.profile.save()

    def profile_url(self):
        return reverse(
            "api:profile-detail",
            kwargs={"username": self.owner.username},
        )

    def get_csrf_token(self):
        response = self.client.get(reverse("api:csrf"))
        return response.json()["csrfToken"]

    def test_anonymous_user_can_view_public_profile(self):
        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["username"],
            "traveler",
        )
        self.assertEqual(
            response.json()["bio"],
            "Exploring the world.",
        )
        self.assertNotIn("email", response.json())

    def test_anonymous_user_sees_limited_private_profile(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["username"],
            "traveler",
        )
        self.assertNotIn("bio", response.json())
        self.assertNotIn("email", response.json())

    def test_unapproved_user_sees_limited_private_profile(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("bio", response.json())

    def test_approved_follower_can_view_private_profile(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        Follow.objects.create(
            follower=self.viewer,
            following=self.owner,
        )

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["bio"],
            "Exploring the world.",
        )

    def test_pending_follow_request_does_not_grant_access(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        FollowRequest.objects.create(
            requester=self.viewer,
            recipient=self.owner,
            status=FollowRequest.Status.PENDING,
        )

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("bio", response.json())

    def test_blocked_viewer_cannot_view_profile(self):
        UserBlock.objects.create(
            blocker=self.owner,
            blocked=self.viewer,
        )

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 404)

    def test_blocking_owner_cannot_view_profile(self):
        UserBlock.objects.create(
            blocker=self.viewer,
            blocked=self.owner,
        )

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 404)

    def test_owner_can_view_own_private_profile(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        self.client.force_login(self.owner)

        response = self.client.get(reverse("api:profile-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["bio"],
            "Exploring the world.",
        )

    def test_anonymous_user_cannot_access_my_profile(self):
        response = self.client.get(reverse("api:profile-me"))

        self.assertEqual(response.status_code, 403)

    def test_owner_can_update_profile(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={
                "display_name": "World Traveler",
                "bio": "New adventures ahead.",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        self.owner.profile.refresh_from_db()

        self.assertEqual(
            self.owner.profile.display_name,
            "World Traveler",
        )
        self.assertEqual(
            self.owner.profile.bio,
            "New adventures ahead.",
        )

    def test_profile_update_requires_csrf(self):
        self.client.force_login(self.owner)

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"bio": "Unauthorized update"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

        self.owner.profile.refresh_from_db()

        self.assertEqual(
            self.owner.profile.bio,
            "Exploring the world.",
        )

    def test_user_cannot_update_another_profile(self):
        self.client.force_login(self.viewer)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"bio": "Attempted overwrite"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        self.owner.profile.refresh_from_db()
        self.viewer.profile.refresh_from_db()

        self.assertEqual(
            self.owner.profile.bio,
            "Exploring the world.",
        )
        self.assertEqual(
            self.viewer.profile.bio,
            "Attempted overwrite",
        )

    def test_public_profile_does_not_expose_email(self):
        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("email", response.json())

    def test_nonexistent_profile_returns_404(self):
        response = self.client.get(
            reverse(
                "api:profile-detail",
                kwargs={"username": "doesnotexist"},
            )
        )

        self.assertEqual(response.status_code, 404)



    def test_anonymous_user_cannot_update_profile(self):
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"bio": "Unauthorized update"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 403)

        self.owner.profile.refresh_from_db()
        self.assertEqual(
            self.owner.profile.bio,
            "Exploring the world.",
        )

    def test_owner_can_change_profile_privacy(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"is_private": True},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        self.owner.profile.refresh_from_db()
        self.assertTrue(self.owner.profile.is_private)

        self.client.logout()

        public_response = self.client.get(self.profile_url())

        self.assertEqual(public_response.status_code, 200)
        self.assertNotIn("bio", public_response.json())

    def test_profile_update_rejects_excessive_display_name(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"display_name": "A" * 101},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 400)

        self.owner.profile.refresh_from_db()
        self.assertEqual(
            self.owner.profile.display_name,
            "Travel Explorer",
        )

    def test_profile_update_rejects_excessive_bio(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={"bio": "A" * 501},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 400)

        self.owner.profile.refresh_from_db()
        self.assertEqual(
            self.owner.profile.bio,
            "Exploring the world.",
        )

    def test_profile_update_cannot_change_username(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={
                "username": "hackedusername",
                "bio": "Updated biography.",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        self.owner.refresh_from_db()
        self.assertEqual(self.owner.username, "traveler")

    def test_profile_update_cannot_change_email(self):
        self.client.force_login(self.owner)
        token = self.get_csrf_token()

        response = self.client.patch(
            reverse("api:profile-me"),
            data={
                "email": "changed@example.com",
                "bio": "Updated biography.",
            },
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)

        self.owner.refresh_from_db()
        self.assertEqual(
            self.owner.email,
            "traveler@example.com",
        )

    def test_blocked_user_cannot_view_private_profile(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        Follow.objects.create(
            follower=self.viewer,
            following=self.owner,
        )

        UserBlock.objects.create(
            blocker=self.owner,
            blocked=self.viewer,
        )

        self.client.force_login(self.viewer)

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 404)

    def test_private_profile_does_not_expose_bio_to_anonymous_user(self):
        self.owner.profile.is_private = True
        self.owner.profile.save()

        response = self.client.get(self.profile_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("bio", response.json())
        self.assertNotIn("email", response.json())
