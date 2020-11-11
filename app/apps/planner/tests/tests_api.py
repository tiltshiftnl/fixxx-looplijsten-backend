from constance.test import override_config
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.settings.const import EXAMPLE_PLANNER_SETTINGS
from app.utils.unittest_helpers import (
    get_authenticated_client,
    get_unauthenticated_client,
)


class SettingsPlannerViewSet(APITestCase):
    """
    Tests for the API endpoints for retrieving planner settings
    """

    def get_url(self):
        return reverse("settings-planner-list")

    def test_unauthenticated_request(self):
        """
        An unauthenticated request should not be possible
        """

        url = self.get_url()
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(PLANNER_SETTINGS='{"foo_settings": "foo"}')
    def test_settings(self):
        """
        Should return the PLANNER_SETTINGS value
        """
        url = self.get_url()
        client = get_authenticated_client()
        response = client.get(url)

        expected_response = {"foo_settings": "foo"}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)

    # TODO: rewrite for new team settings
    # @override_config(PLANNER_SETTINGS="")
    # def test_no_settings_saved(self):
    #     """
    #     Should return the default example planner settings if PLANNER_SETTINGS aren't set
    #     """
    #     url = self.get_url()
    #     client = get_authenticated_client()
    #     response = client.get(url)

    #     expected_response = EXAMPLE_PLANNER_SETTINGS
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(response.json(), expected_response)
