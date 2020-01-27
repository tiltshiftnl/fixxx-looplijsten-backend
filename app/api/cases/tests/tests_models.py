"""
Tests for cases models
"""
from unittest.mock import Mock
from api.cases.models import Case
from django.test import TestCase

class CaseModelTest(TestCase):

    def test_create_case_object(self):
        """
        A Case object can be created
        """

        self.assertEqual(Case.objects.count(), 0)
        Case.objects.create(case_id='FOO')
        self.assertEqual(Case.objects.count(), 1)

    def test_case_object_string(self):
        """
        A Case oject's string representation is the same as it's case_id
        """

        CASE_ID = 'CASE ID FOO'
        case = Case.objects.create(case_id=CASE_ID)
        self.assertEquals(case.__str__(), CASE_ID)

    def test_case_object_bwv_data(self):
        """
        The bwv_data property calls get_case util function using the Case object's ID
        """
        CASE_ID = 'CASE ID FOO'
        case = Case.objects.create(case_id=CASE_ID)

        # This patches the objects __get_case__ function
        MOCK_BWV_DATA = 'FOO BWV'
        case.__get_case__ = Mock()
        case.__get_case__.return_value = MOCK_BWV_DATA

        bwv_data = case.bwv_data

        self.assertEquals(bwv_data, MOCK_BWV_DATA)
        case.__get_case__.assert_called_with(CASE_ID)
