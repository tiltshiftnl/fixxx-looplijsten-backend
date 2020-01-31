"""
Tests for helpers
"""
from django.test import TestCase
from api.users.utils import generate_username

class GenerateUsernameTest(TestCase):

    def test_generate_username_space_normalize(self):
        """
        Normalizes the given string
        """
        username = generate_username('株式会社ＫＡＤＯＫＡＷＡ Ｆｕｔｕｒｅ Ｐｕｂｌｉｓｈｉｎｇ')

        self.assertEqual(username, '株式会社KADOKAWA Future Publishing')

    def test_generate_username_max_length(self):
        """
        Shortens to max 150 characters
        """

        username_input = ['x' for i in range(0, 300)]
        username_input = ''.join(username_input)

        username = generate_username(username_input)

        self.assertEquals(150, len(username))
