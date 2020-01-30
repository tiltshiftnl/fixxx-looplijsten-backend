from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from constance.test import override_config
from app.utils.unittest_helpers import get_authenticated_client, get_unauthenticated_client

class IsAuthenticatedViewTest(APITestCase):
    """
    Tests for the API endpoints for IsAuthenticatedView
    """

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        An request to check authentication should not be possible if
        the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('is-authenticated')
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_requests(self):
        """
        is_authenticated is true when user is not logged in
        """
        url = reverse('is-authenticated')
        client = get_authenticated_client()
        response = client.get(url)

        expected_response = {
            'is_authenticated': True
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)

    def test_unauthenticated_requests(self):
        """
        is_authenticated false true when user is not logged in
        """
        url = reverse('is-authenticated')
        client = get_unauthenticated_client()
        response = client.get(url)

        expected_response = {
            'is_authenticated': False
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)
