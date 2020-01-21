"""
Tests for safey_lock
"""
from django.test import TestCase
from django.http import Http404
from constance.test import override_config
from utils.safety_lock import safety_lock

MOCK_RETURN = 'Foo'
def mock_function():
    return MOCK_RETURN

class SafetyLockTest(TestCase):

    def test_unlocked(self):
        """
        Executes the (decorated) function
        """
        result = safety_lock(mock_function)()
        self.assertEqual(result, MOCK_RETURN)

    @override_config(ALLOW_DATA_ACCESS=False)
    def test_locked(self):
        """
        Doesn not executes the (decorated) function, and raises 404 error
        """
        with self.assertRaises(Http404):
            safety_lock(mock_function)()
