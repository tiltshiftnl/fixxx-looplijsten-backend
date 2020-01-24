"""
Tests for BAG queries
"""
from django.test import TestCase
from django.conf import settings
from utils.queries_bag_api import get_bag_search_query, do_bag_search_address, do_bag_search_id
from unittest.mock import patch

# TODO: write tests for get_bag_data

class GetBagSearchQueryTest(TestCase):

    def test_get_search_query_basic(self):
        """
        Returns a search query given a postal code and a house number
        """
        address = {
            'postcode': 'postcode_foo',
            'hsnr': 'hsnr_foo',
        }

        result = get_bag_search_query(address)

        self.assertEquals(result, 'postcode_foo hsnr_foo')

    def test_get_search_query_letter(self):
        """
        Returns a search query given a postal code, a house number, and a letter
        """
        address = {
            'postcode': 'postcode_foo',
            'hsnr': 'hsnr_foo',
            'hsltr': 'hsltr_foo'
        }

        result = get_bag_search_query(address)

        self.assertEquals(result, 'postcode_foo hsnr_foo hsltr_foo')

    def test_get_search_query_addition(self):
        """
        Returns a search query given a postal code, a house number, and an addition
        """
        address = {
            'postcode': 'postcode_foo',
            'hsnr': 'hsnr_foo',
            'toev': 'toev_foo'
        }

        result = get_bag_search_query(address)

        self.assertEquals(result, 'postcode_foo hsnr_foo toev_foo')

    def test_get_search_query_alll(self):
        """
        Returns a search query given all optional parameters
        """
        address = {
            'postcode': 'postcode_foo',
            'hsnr': 'hsnr_foo',
            'hsltr': 'hsltr_foo',
            'toev': 'toev_foo'
        }

        result = get_bag_search_query(address)

        self.assertEquals(result, 'postcode_foo hsnr_foo hsltr_footoev_foo')


class DoBagSearchAddressTest(TestCase):

    @patch('utils.queries_bag_api.get_bag_search_query')
    @patch('requests.get')
    def test_do_bag_search_address(self, mock_requests_get, mock_get_bag_search_query):
        """
        Does a get request to the BAG API using an address search query
        """

        address = 'Foo'
        mock_get_bag_search_query.return_value = 'Foo Query'

        do_bag_search_address(address)

        # The BAG search query is retrieved
        mock_get_bag_search_query.assert_called()

        # The GET request is performed
        mock_requests_get.assert_called_with(
            settings.BAG_API_SEARCH_URL,
            params={'q': 'Foo Query'}
        )


class DoBagSearchIdTest(TestCase):

    @patch('requests.get')
    def test_do_bag_search_id(self, mock_requests_get):
        """
        Does a get request to the BAG API using a BAG ID
        """

        address = {
            'landelijk_bag': 'Foo ID'
        }

        do_bag_search_id(address)

        # The GET request is performed
        mock_requests_get.assert_called_with(
            settings.BAG_API_SEARCH_URL,
            params={'q': 'Foo ID'}
        )
