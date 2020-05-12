from unittest.mock import patch

from constance.test import override_config
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.itinerary.models import Itinerary, ItinerarySettings
from app.utils.unittest_helpers import get_authenticated_client, get_unauthenticated_client, get_test_user


class ItineraryViewsGetTest(APITestCase):
    """
    Tests for the API endpoint for retrieving itineraries
    """
    maxDiff = None

    def test_unauthenticated_request_get(self):
        """
        An unauthenticated request should not be possible
        """

        url = reverse('itinerary-list')
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request_get(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_itinerary_get(self):
        """
        Should succeed and return no itineraries (none have been created)
        """
        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_response_json = {
            "itineraries": []
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_json)

    def test_itinerary_without_user_get(self):
        """
        Should return an empty response if no users are associated with itinerary
        """
        Itinerary.objects.create()
        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_response_json = {
            "itineraries": []
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response_json)

    def test_itinerary_with_user_get(self):
        """
        Should return a filled response if the authenticed user is associated with itinerary
        """
        itinerary = Itinerary.objects.create()
        user = get_test_user()
        itinerary.add_team_members([user.id])

        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_respsonse = {
            'itineraries': [
                {
                    'id': itinerary.id,
                    'created_at': str(itinerary.created_at),
                    'team_members': [
                        {'id': itinerary.team_members.all()[0].id, 'user': {
                            'id': str(user.id),
                            'email': user.email,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'full_name': user.full_name}}],
                    'items': [],
                    'settings': None}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_respsonse)

    def test_multiple_itineraries_for_user(self):
        """
        Should return multiple itineraries that are associated with user
        """
        itinerary_a = Itinerary.objects.create()
        itinerary_b = Itinerary.objects.create()
        user = get_test_user()
        itinerary_a.add_team_members([user.id])
        itinerary_b.add_team_members([user.id])

        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(url)

        expected_respsonse = {
            'itineraries': [
                {
                    'id': itinerary_a.id,
                    'created_at': str(itinerary_a.created_at),
                    'team_members': [
                        {'id': itinerary_a.team_members.all()[0].id,
                         'user': {
                             'id': str(user.id),
                             'email': user.email,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'full_name': user.full_name}}],
                    'items': [],
                    'settings': None
                },
                {
                    'id': itinerary_b.id,
                    'created_at': str(itinerary_b.created_at),
                    'team_members': [
                        {'id': itinerary_b.team_members.all()[0].id,
                         'user': {
                             'id': str(user.id),
                             'email': user.email,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'full_name': user.full_name}}],
                    'items': [],
                    'settings': None
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_respsonse)

    @freeze_time("2020-04-02")
    def test_itinerary_with_date(self):
        """
        Should return itineraries for a given date if created_at date is included
        """
        itinerary = Itinerary.objects.create()
        user = get_test_user()
        itinerary.add_team_members([user.id])

        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(
            url,
            {'created_at': "2020-04-02"}
        )

        expected_respsonse = {
            'itineraries': [
                {
                    'id': itinerary.id,
                    'created_at': "2020-04-02",
                    'team_members': [
                        {'id': itinerary.team_members.all()[0].id,
                         'user': {
                             'id': str(user.id),
                             'email': user.email,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'full_name': user.full_name}}],
                    'items': [],
                    'settings': None}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_respsonse)

    @freeze_time("2020-04-02")
    def test_no_itineraries_with_date(self):
        """
        Returns an empty list if no itineraries exist for given date
        """
        itinerary = Itinerary.objects.create()
        user = get_test_user()
        itinerary.add_team_members([user.id])

        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.get(
            url,
            {'created_at': "2022-04-02"}
        )
        expected_respsonse = {'itineraries': []}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_respsonse)


class ItineraryViewsCreateTest(APITestCase):
    """
    Tests for the API endpoint for creating itineraries
    """
    maxDiff = None

    def test_unauthenticated_request_post(self):
        """
        An unauthenticated request should not be possible
        """

        url = reverse('itinerary-list')
        client = get_unauthenticated_client()
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request_post(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('itinerary-list')
        client = get_authenticated_client()
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        """
        Should succeed and create an itinerary
        """
        self.assertEqual(Itinerary.objects.count(), 0)

        url = reverse('itinerary-list')
        client = get_authenticated_client()
        user = get_test_user()

        response = client.post(
            url,
            {
                "team_members": [{"user": {"id": user.id}}],
                "settings": {
                    "opening_date": "2020-04-24",
                    "target_length": 8,
                }
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Itinerary.objects.count(), 1)


class ItineraryViewsDeleteTest(APITestCase):
    """
    Tests for the API endpoint for deleting itineraries
    """
    maxDiff = None

    def test_unauthenticated_request_delete(self):
        """
        An unauthenticated request should not be possible
        """
        itinerary = Itinerary.objects.create()
        url = reverse('itinerary-detail', kwargs={'pk': itinerary.id})

        client = get_unauthenticated_client()
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request_delete(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        itinerary = Itinerary.objects.create()
        url = reverse('itinerary-detail', kwargs={'pk': itinerary.id})

        client = get_authenticated_client()
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        """
        Removes a itinerary object using a delete request
        """
        itinerary = Itinerary.objects.create()

        url = reverse('itinerary-detail', kwargs={'pk': itinerary.id})
        client = get_authenticated_client()
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Itinerary.objects.count(), 0)


class ItineraryViewsSuggestionsTest(APITestCase):
    """
    Tests for the API endpoint for retrieving suggestions
    """

    def test_unauthenticated_request_get_suggestions(self):
        """
        An unauthenticated request should not be possible
        """
        itinerary = Itinerary.objects.create()

        url = reverse('itinerary-suggestions', kwargs={'pk': itinerary.id})
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request_get_suggestions(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        itinerary = Itinerary.objects.create()

        url = reverse('itinerary-suggestions', kwargs={'pk': itinerary.id})
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('api.itinerary.views.Itinerary.get_suggestions')
    def test_get_suggestions(self, mock_get_suggestions):
        """
        A working authenticated request should return suggestions
        """
        mock_get_suggestions.return_value = 'FOO_SUGGESTIONS'

        itinerary = Itinerary.objects.create()
        ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)

        url = reverse('itinerary-suggestions', kwargs={'pk': itinerary.id})
        client = get_authenticated_client()
        response = client.get(url)

        expected_response = {
            'cases': 'FOO_SUGGESTIONS'
        }
        self.assertEqual(expected_response, response.json())
