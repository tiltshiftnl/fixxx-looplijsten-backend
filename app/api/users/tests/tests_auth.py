"""
Tests for authentication.
Note: It's possible to write more extensive tests for the auth module, but the main
intention with these tests is to make sure a User is created of synched when authenticating
with the OIDC provider
"""
from constance.test import override_config
from api.users.auth import OIDCAuthenticationBackend
from unittest.mock import Mock
from django.test import TestCase
from django.http.response import Http404
from django.core.exceptions import SuspiciousOperation
from app.utils.unittest_helpers import get_test_user

MOCK_AUTH_CODE = 'FOO_CODE'
MOCK_AUTH_REQUEST = Mock()
MOCK_AUTH_REQUEST.data = Mock()
MOCK_AUTH_REQUEST.data.code = MOCK_AUTH_CODE

class AuthTest(TestCase):

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_safety_locked_request(self):
        """
        A request should not be possible if the safety_lock (ALLOW_DATA_ACCESS) is on
        """
        authentication_backend = OIDCAuthenticationBackend()

        with self.assertRaises(Http404):
            authentication_backend.authenticate(MOCK_AUTH_REQUEST)

    def test_no_code_in_request(self):
        """
        An authentication without given data and access code will not do anything
        """

        authentication_backend = OIDCAuthenticationBackend()

        authentication_backend.get_token = Mock()
        authentication_backend.verify_token = Mock()
        authentication_backend.store_tokens = Mock()
        authentication_backend.get_or_create_user = Mock()

        request = {}
        result = authentication_backend.authenticate(request)

        self.assertIsNone(result)
        authentication_backend.get_token.assert_not_called()
        authentication_backend.verify_token.assert_not_called()
        authentication_backend.store_tokens.assert_not_called()
        authentication_backend.get_or_create_user.assert_not_called()

    def test_user_created(self):
        """
        An succesful authentication should create a new user
        """
        authentication_backend = OIDCAuthenticationBackend()

        authentication_backend.get_token = Mock()
        authentication_backend.store_tokens = Mock()

        # Mock verify token and payload
        authentication_backend.verify_token = Mock()
        authentication_backend.verify_token.return_value = {
            'payload_foo': 'foo_data'
        }

        # Mock user creation
        FOO_USER = get_test_user()
        authentication_backend.get_or_create_user = Mock()
        authentication_backend.get_or_create_user.return_value = FOO_USER

        authenticated_result = authentication_backend.authenticate(MOCK_AUTH_REQUEST)

        authentication_backend.get_token.assert_called_once()
        authentication_backend.verify_token.assert_called_once()
        authentication_backend.store_tokens.assert_called_once()

        # Most importantly, the get_or_create_user function is called, and it's return value is given
        authentication_backend.get_or_create_user.assert_called_once()
        self.assertEquals(authenticated_result, FOO_USER)

    def test_verification_fails(self):
        """
        No user is created if token verification fails
        """
        authentication_backend = OIDCAuthenticationBackend()

        authentication_backend.get_token = Mock()
        authentication_backend.store_tokens = Mock()
        authentication_backend.get_or_create_user = Mock()

        # Mock verify token and payload
        # This mock raises an 'SuspiciousOperation' exception
        authentication_backend.verify_token = Mock(side_effect=SuspiciousOperation('Token not verified'))

        # Call the authentication
        authenticated_result = authentication_backend.authenticate(MOCK_AUTH_REQUEST)

        # Verify is called
        authentication_backend.verify_token.assert_called_once()

        # But the user creation not
        authentication_backend.get_or_create_user.assert_not_called()
        self.assertIsNone(authenticated_result)