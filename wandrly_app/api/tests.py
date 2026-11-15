from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.test import APIClient


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
