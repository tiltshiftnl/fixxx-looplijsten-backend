# TODO: Incorporate fraud_prediction

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        An authenticated request fails if the requested id's doesn't have a wng_id or adres_id
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
    def test_authenticated_requests_succeeds(self, mock_q, mock_bag_api, mock_brk_api):
        """
        An authenticated request succeeds and contains all the necessary data
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

        FOO_STATEMENTS = 'FOO_STATEMENTS'
        mock_q.get_statements = Mock(return_value=FOO_STATEMENTS)

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
            'fraud_prediction': None,
            'statements': FOO_STATEMENTS,
            'vakantie_verhuur': FOO_RENTAL_INFORMATION,
            'bag_data': FOO_BAG_DATA,
            'brk_data': FOO_BRK_DATA,
            'related_cases': FOO_RELATED_CASES
        }

        self.assertEquals(response.json(), expected_response)


class CaseSearchViewSetTest(APITestCase):
    """
    Tests for the API endpoint for searching cases
    """

    MOCK_SEARCH_QUERY_PARAMETERS = {
        'postalCode': 'FOO_POSTAL_CODE',
        'streetNumber': 'FOO_STREET_NUMBER',
        'suffix': 'FOO_SUFFIX'
    }

    def test_unauthenticated_request(self):
        """
        An unauthenticated search should not be possible
        """
        url = reverse('search-list')
        client = get_unauthenticated_client()
        response = client.get(url, self.MOCK_SEARCH_QUERY_PARAMETERS)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        An authenticated search should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        url = reverse('search-list')
        client = get_authenticated_client()
        response = client.get(url, self.MOCK_SEARCH_QUERY_PARAMETERS)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('api.cases.views.q')
    def test_search_without_postal_code(self, mock_q):
        """
        An authenticated search should fail if postal code is not available
        """
        url = reverse('search-list')
        client = get_authenticated_client()

        MOCK_SEARCH_QUERY_PARAMETERS = self.MOCK_SEARCH_QUERY_PARAMETERS.copy()
        MOCK_SEARCH_QUERY_PARAMETERS.pop('postalCode')

        # Mock search function
        mock_q.get_search_results = Mock()
        mock_q.get_search_results.return_value = []

        response = client.get(url, MOCK_SEARCH_QUERY_PARAMETERS)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('api.cases.views.q')
    def test_search_without_street_number(self, mock_q):
        """
        An authenticated search should fail if street number is not available
        """
        url = reverse('search-list')
        client = get_authenticated_client()

        MOCK_SEARCH_QUERY_PARAMETERS = self.MOCK_SEARCH_QUERY_PARAMETERS.copy()
        MOCK_SEARCH_QUERY_PARAMETERS.pop('postalCode')

        # Mock search function
        mock_q.get_search_results = Mock()
        mock_q.get_search_results.return_value = []

        response = client.get(url, MOCK_SEARCH_QUERY_PARAMETERS)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('api.cases.views.q')
    def test_search(self, mock_q):
        """
        An authenticated search works
        """
        url = reverse('search-list')
        client = get_authenticated_client()

        # Mock search function
        FOO_SEARCH_RESULTS = []
        mock_q.get_search_results = Mock(return_value=FOO_SEARCH_RESULTS)

        response = client.get(url, self.MOCK_SEARCH_QUERY_PARAMETERS)

        # Tests if the search function was called with all the given parameters
        mock_q.get_search_results.assert_called_with(*self.MOCK_SEARCH_QUERY_PARAMETERS.values())

        # Tests if a success response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Tests if the response contains the mock data
        self.assertEqual(response.json(), {'cases': FOO_SEARCH_RESULTS})

    @patch('api.cases.views.q')
    def test_search_without_suffix(self, mock_q):
        """
        An authenticated search works without optional suffix
        """
        url = reverse('search-list')
        client = get_authenticated_client()

        # Mock search function
        FOO_SEARCH_RESULTS = []
        mock_q.get_search_results = Mock(return_value=FOO_SEARCH_RESULTS)

        MOCK_SEARCH_QUERY_PARAMETERS = self.MOCK_SEARCH_QUERY_PARAMETERS.copy()
        MOCK_SEARCH_QUERY_PARAMETERS.pop('suffix')

        response = client.get(url, MOCK_SEARCH_QUERY_PARAMETERS)

        # Tests if the search function was called with all the given parameters
        mock_q.get_search_results.assert_called_with(*MOCK_SEARCH_QUERY_PARAMETERS.values(), '')

        # Tests if a success response code is given
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Tests if the response contains the mock data
        self.assertEqual(response.json(), {'cases': FOO_SEARCH_RESULTS})

    @patch('api.cases.views.q')
    def test_search_with_teams_array(self, mock_q):
        """
        The cases in a search result should contain a teams array
        """
        url = reverse('search-list')
        client = get_authenticated_client()

        CASE_ID = 'FOO-ID'

        # Mock search function
        FOO_SEARCH_RESULTS = [{'case_id': CASE_ID}]
        mock_q.get_search_results = Mock(return_value=FOO_SEARCH_RESULTS)

        response = client.get(url, self.MOCK_SEARCH_QUERY_PARAMETERS)

        # Tests if the response contains the mock data with an added teams array
        expected_response = {'cases': [{'case_id': CASE_ID, 'fraud_prediction': None, 'teams': []}]}
        self.assertEqual(response.json(), expected_response)
