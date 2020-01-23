"""
Tests for accesslogs middleware
"""
import django
from django.db import Error
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, Mock
from api.health.views import health_default, health_bwv, health_generic, SUCCESS_MESSAGE_DEFAULT
from api.health.views import ERROR_MESSAGE_DEFAULT, SUCCESS_MESSAGE_BWV, ERROR_MESSAGE_BWV

DATABASE_NAME = 'foo'

class AccessLogsMiddlewareTest(TestCase):

    @patch.dict('django.db.connections', {DATABASE_NAME: Mock()})
    def test_health_generic_success(self):
        """
        Calls the generic health function successfully, and returns 200 status code
        """
        cursor_mock = Mock()
        django.db.connections[DATABASE_NAME].cursor = cursor_mock

        REQUEST = Mock()
        SUCCESS_MESSAGE = 'foo success'
        ERROR_MESSAGE = 'foo error'

        response = health_generic(REQUEST, DATABASE_NAME, SUCCESS_MESSAGE, ERROR_MESSAGE)

        self.assertEqual(response.status_code, 200)

    @patch.dict('django.db.connections', {DATABASE_NAME: Mock()})
    def test_health_generic_error(self):
        """
        Calls the generic health function, fails and returns the 500 status code
        """
        def cursor_mock():
            raise Error('Mock Exception')

        django.db.connections[DATABASE_NAME].cursor = cursor_mock

        REQUEST = Mock()
        SUCCESS_MESSAGE = 'foo success'
        ERROR_MESSAGE = 'foo error'

        response = health_generic(REQUEST, DATABASE_NAME, SUCCESS_MESSAGE, ERROR_MESSAGE)

        self.assertEqual(response.status_code, 500)

    @patch('api.health.views.health_generic')
    def test_health_default(self, mock_health_generic):
        """
        Calls the generic health function with the default database from settings
        """
        request = Mock()
        health_default(request)

        mock_health_generic.assert_called_with(
            request=request,
            database_name=settings.DEFAULT_DATABASE_NAME,
            success_message=SUCCESS_MESSAGE_DEFAULT,
            error_message=ERROR_MESSAGE_DEFAULT
        )

    @patch('api.health.views.health_generic')
    def test_health_bwv(self, mock_health_generic):
        """
        Calls the generic health function with the bwv database from settings
        """
        request = Mock()
        health_bwv(request)

        mock_health_generic.assert_called_with(
            request=request,
            database_name=settings.BWV_DATABASE_NAME,
            success_message=SUCCESS_MESSAGE_BWV,
            error_message=ERROR_MESSAGE_BWV
        )
