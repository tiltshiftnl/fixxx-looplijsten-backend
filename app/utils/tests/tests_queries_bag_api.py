"""
Tests for BAG queries
"""
from django.test import TestCase
from utils.queries_bag_api import get_bag_search_query

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
