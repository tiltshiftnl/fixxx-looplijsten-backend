from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from constance.test import override_config
from app.utils.unittest_helpers import get_authenticated_client, get_unauthenticated_client
from app.api.planner.const import PROJECTS, STAGES

class ConstantsProjectsViewSet(APITestCase):
    """
    Tests for the API endpoints for retrieving project constants
    """

    def test_unauthenticated_request(self):
        """
        An unauthenticated request should not be possible
        """

        url = reverse('constants-projects-list')
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('constants-projects-list')
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_requests(self):
        """
        An authenticated request should return the projects constants in a dictionary
        """
        url = reverse('constants-projects-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_response = {
            'constants': PROJECTS
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)


class ConstantsStadiaViewSet(APITestCase):
    """
    Tests for the API endpoints for retrieving stadium constants
    """

    def test_unauthenticated_request(self):
        """
        An unauthenticated request should not be possible
        """

        url = reverse('constants-stadia-list')
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('constants-stadia-list')
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_requests(self):
        """
        An authenticated request should return the projects constants in a dictionary
        """
        url = reverse('constants-stadia-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_response = {
            'constants': STAGES
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)
