
"""
Tests for query_helpers
"""
from unittest.mock import patch, Mock

from django.db import Error
from django.test import TestCase

from utils.query_helpers import return_first_or_empty, do_query


# TODO: Write tests for query_to_list

class ReturnFirstOrEmptyTest(TestCase):
    def test_should_return_first(self):
        '''
        Should return the first object in the list
        '''
        foo_object_a = {'foo_a': 'foo_a_value'}
        foo_object_b = {'foo_b': 'foo_b_value'}

        result = return_first_or_empty([foo_object_a, foo_object_b])
        self.assertEqual(foo_object_a, result)

    def test_should_return_empty(self):
        '''
        Should return an empty object if an empty list is given
        '''
        result = return_first_or_empty([])
        self.assertEqual(result, {})


class DoQueryTest(TestCase):
    @patch('utils.query_helpers.__get_bwv_cursor__')
    @patch('utils.query_helpers.query_to_list')
    def test_do_query(self, mock_query_to_list, mock_get_bwv_cursor):
        '''
        Should execute the database cursor using given query
        '''
        bwv_cursor = Mock()
        mock_get_bwv_cursor.return_value = bwv_cursor

        QUERY = 'SELECT * FROM table_name'
        args = {'foo': 'foo'}
        do_query(QUERY, args)

        mock_query_to_list.assert_called()
        bwv_cursor.execute.assert_called_with(QUERY, args)

    @patch('utils.query_helpers.__get_bwv_cursor__')
    @patch('utils.query_helpers.query_to_list')
    def test_do_query_no_args(self, mock_query_to_list, mock_get_bwv_cursor):
        '''
        Should execute the database cursor using given query when no args arge given
        '''
        bwv_cursor = Mock()
        mock_get_bwv_cursor.return_value = bwv_cursor

        QUERY = 'SELECT * FROM table_name'
        do_query(QUERY)

        mock_query_to_list.assert_called()
        bwv_cursor.execute.assert_called_with(QUERY, None)

    @patch('utils.query_helpers.__get_bwv_cursor__')
    def test_do_query_fails(self, mock_get_bwv_cursor):
        '''
        Should return empty list when query execution fails
        '''

        def failing_execute_mock(query):
            raise Error('Mock Exception')

        bwv_cursor = Mock()
        bwv_cursor.execute = failing_execute_mock
        mock_get_bwv_cursor.return_value = bwv_cursor

        QUERY = 'SELECT * FROM table_name'
        result = do_query(QUERY)

        self.assertEqual(result, [])
