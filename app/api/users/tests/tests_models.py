"""
Tests for cases models
"""
from api.users.models import User
from django.test import TestCase
from django.db import transaction

USER_EMAIL = 'foo@foo.com'

class UserModelTest(TestCase):

    def test_create_user(self):
        """
        A User can be created
        """
        self.assertEqual(User.objects.count(), 0)
        User.objects.create(email=USER_EMAIL)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_existing_email(self):
        """
        A User cannot be created if another User has the same email
        """
        self.assertEqual(User.objects.count(), 0)
        User.objects.create(email=USER_EMAIL)

        with transaction.atomic():
            with self.assertRaises(Exception):
                User.objects.create(email=USER_EMAIL)

        self.assertEqual(User.objects.count(), 1)

    def test_create_multiple_users(self):
        """
        Multiple users can be created as long as their emails differ
        """
        self.assertEqual(User.objects.count(), 0)
        User.objects.create(email=USER_EMAIL)
        User.objects.create(email='foo-other-email@foo.com')
        self.assertEqual(User.objects.count(), 2)

    def test_username(self):
        """
        A User's username is equal to it's email
        (with the exception of when the email is normalized to generate the username. 
        This is tested in tests_util.py)
        """
        USER_EMAIL = 'foo@foo.com'
        user = User.objects.create(email=USER_EMAIL)

        self.assertEqual(user.username, USER_EMAIL)
        self.assertEqual(user.email, USER_EMAIL)

    def test_string_representation(self):
        """
        A User object is displayed as its email
        """
        USER_EMAIL = 'foo@foo.com'
        user = User.objects.create(email=USER_EMAIL)

        self.assertEqual(user.__str__(), USER_EMAIL)

    def test_credentials(self):
        """
        A User does not have staff or superuser credentials
        """
        USER_EMAIL = 'foo@foo.com'
        user = User.objects.create(email=USER_EMAIL)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
