from unittest.mock import patch, Mock
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from constance.test import override_config
from app.utils.unittest_helpers import get_authenticated_client, get_unauthenticated_client

class CaseViewSetTest(APITestCase):
    """
    Tests for the API endpoints for retrieving case data
    """

    def test_unauthenticated_request(self):
        """
        An unauthenticated request should not be possible
        """

        url = reverse('case-detail', kwargs={'pk': 'foo'})
        client = get_unauthenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        An authenticated request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('case-detail', kwargs={'pk': 'foo'})
        client = get_authenticated_client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('api.cases.views.brk_api')
    @patch('api.cases.views.bag_api')
    @patch('api.cases.views.q')
    def test_authenticated_requests_no_case(self, mock_q, mock_bag_api, mock_brk_api):
        """
        # An authenticated request fails if the requested id's doesn't have a wng_id or adres_id
        """

        mock_q.get_related_case_ids.return_value = {}

        MOCK_CASE_ID = 'FOO_ID'
        url = reverse('case-detail', kwargs={'pk': MOCK_CASE_ID})
        client = get_authenticated_client()
        response = client.get(url)

        # Makes sure the get_related_case_ids was called using the given pk
        mock_q.get_related_case_ids.assert_called_with(MOCK_CASE_ID)

        # The response returns a 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('api.cases.views.brk_api')
    @patch('api.cases.views.bag_api')
    @patch('api.cases.views.q')
    def test_authenticated_requests_no_case(self, mock_q, mock_bag_api, mock_brk_api):
        """
        # An authenticated request succeeds and contains all the necessary data
        """

        mock_q.get_related_case_ids.return_value = {
            'wng_id': 'FOO_WNG_D',
            'adres_id': 'FOO_ADRES_ID',
        }

        FOO_BAG_DATA = {'verblijfsobjectidentificatie': 'FOO_BAG_DATA_ID'}
        mock_bag_api.get_bag_data = Mock(return_value=FOO_BAG_DATA)

        FOO_BWV_HOTLINE_BEVINDINGEN = 'FOO_BWV_HOTLINE_BEVINDINGEN'
        mock_q.get_bwv_hotline_bevinding = Mock(return_value=FOO_BWV_HOTLINE_BEVINDINGEN)

        FOO_BWV_HOTLINE_MELDING = 'FOO_BWV_HOTLINE_MELDING'
        mock_q.get_bwv_hotline_melding = Mock(return_value=FOO_BWV_HOTLINE_MELDING)

        FOO_BWV_PERSONEN = 'FOO_BWV_PERSONEN'
        mock_q.get_bwv_personen = Mock(return_value=FOO_BWV_PERSONEN)

        FOO_IMPORT_ADRES = 'FOO_IMPORT_ADRES'
        mock_q.get_import_adres = Mock(return_value=FOO_IMPORT_ADRES)

        FOO_IMPORT_STADIA = 'FOO_IMPORT_STADIA'
        mock_q.get_import_stadia = Mock(return_value=FOO_IMPORT_STADIA)

        FOO_BWV_TEMP = 'FOO_BWV_TEMP'
        mock_q.get_bwv_tmp = Mock(return_value=FOO_BWV_TEMP)

        FOO_RENTAL_INFORMATION = 'FOO_RENTAL_INFORMATION'
        mock_q.get_rental_information = Mock(return_value=FOO_RENTAL_INFORMATION)

        FOO_RELATED_CASES = 'FOO_RELATED_CASES'
        mock_q.get_related_cases = Mock(return_value=FOO_RELATED_CASES)

        FOO_BRK_DATA = 'FOO_BRK_DATA'
        mock_brk_api.get_brk_data = Mock(return_value=FOO_BRK_DATA)

        # Now that everythign is mocked, do the actual request
        MOCK_CASE_ID = 'FOO_ID'
        url = reverse('case-detail', kwargs={'pk': MOCK_CASE_ID})
        client = get_authenticated_client()
        response = client.get(url)

        # The response returns a 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The expected response with all the mocked return data
        expected_response = {
            'bwv_hotline_bevinding': FOO_BWV_HOTLINE_BEVINDINGEN,
            'bwv_hotline_melding': FOO_BWV_HOTLINE_MELDING,
            'bwv_personen': FOO_BWV_PERSONEN,
            'import_adres': FOO_IMPORT_ADRES,
            'import_stadia': FOO_IMPORT_STADIA,
            'bwv_tmp': FOO_BWV_TEMP,
            'vakantie_verhuur': FOO_RENTAL_INFORMATION,
            'bag_data': FOO_BAG_DATA,
            'brk_data': FOO_BRK_DATA,
            'related_cases': FOO_RELATED_CASES
        }

        self.assertEquals(response.json(), expected_response)
