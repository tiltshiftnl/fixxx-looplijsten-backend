from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from freezegun import freeze_time
from datetime import datetime
from unittest.mock import patch, Mock

from api.itinerary.models import Itinerary, ItineraryItem, ItinerarySettings
from api.cases.models import Case
from api.users.models import User

class ItineraryModelTest(TestCase):
    def test_create_itinerary(self):
        '''
        An Itinerary object can be created
        '''
        self.assertEquals(Itinerary.objects.count(), 0)
        Itinerary.objects.create()
        self.assertEquals(Itinerary.objects.count(), 1)

    @freeze_time("2019-12-25")
    def test_creation_date(self):
        '''
        Test if the created_at is current date
        '''
        itinerary = Itinerary.objects.create()
        self.assertEquals(itinerary.created_at, datetime(2019, 12, 25).date())

    def test_add_case(self):
        '''
        add_case function creates itinerary objects assocated with this itinerary
        '''
        itinerary = Itinerary.objects.create()

        self.assertEquals(itinerary.items.count(), 0)
        self.assertEquals(ItineraryItem.objects.count(), 0)

        itinerary.add_case('FOO_CASE_ID_A')
        itinerary.add_case('FOO_CASE_ID_B')

        self.assertEquals(itinerary.items.count(), 2)
        self.assertEquals(ItineraryItem.objects.count(), 2)

    def test_add_case_with_positions(self):
        '''
        add_case with positions
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A', 3)

        self.assertEquals(itinerary.items.all()[0].position, 3)

    def test_add_case_same_position_fail(self):
        '''
        add_case with same positions should fail
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A', 3)

        with self.assertRaises(Exception):
            itinerary.add_case('FOO_CASE_ID_B', 3)

    def test_add_same_cases_fail(self):
        '''
        add_case with same case should fail
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A')

        with self.assertRaises(Exception):
            itinerary.add_case('FOO_CASE_ID_A')

    def test_get_cases(self):
        '''
        get_cases should return the Itinerary's cases
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A')
        itinerary.add_case('FOO_CASE_ID_B')

        cases = itinerary.get_cases()

        self.assertEquals(len(cases), 2)

    def test_get_no_cases(self):
        '''
        get_cases returns no cases if itinerary doesn't have cases
        '''
        itinerary = Itinerary.objects.create()
        cases = itinerary.get_cases()
        self.assertEquals(len(cases), 0)

    @freeze_time("2019-12-25")
    def test_get_cases_for_date(self):
        '''
        Should return cases which are in itineraries for the given date
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A')
        itinerary.add_case('FOO_CASE_ID_B')

        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_C')

        cases = Itinerary.get_cases_for_date('2019-12-25')
        cases_expected = [Case.get('FOO_CASE_ID_A'), Case.get('FOO_CASE_ID_B'), Case.get('FOO_CASE_ID_C')]
        self.assertEquals(cases, cases_expected)

    @freeze_time("2019-12-25")
    def test_get_cases_for_date_empty(self):
        '''
        Should return cases which are in itineraries for the given date
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A')
        itinerary.add_case('FOO_CASE_ID_B')

        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_C')

        # Get cases for another date
        cases = Itinerary.get_cases_for_date('2018-10-20')
        self.assertEquals(cases, [])

    @freeze_time("2019-12-25")
    def test_get_cases_for_date_fail(self):
        '''
        Fails if the date is in the wrong format
        '''
        itinerary = Itinerary.objects.create()
        itinerary.add_case('FOO_CASE_ID_A')

        with self.assertRaises(ValidationError):
            Itinerary.get_cases_for_date('fooo')

    @freeze_time("2019-12-25")
    @patch('api.itinerary.models.get_cases_from_bwv')
    def test_get_unplanned_cases(self, mock_get_cases_from_bwv):
        '''
        Should return cases which are in itineraries for the given date
        '''
        FOO_CASE_ID_A = 'FOO_CASE_ID_A'
        FOO_CASE_ID_B = 'FOO_CASE_ID_B'
        FOO_CASE_ID_C = 'FOO_CASE_ID_C'
        FOO_CASE_ID_D = 'FOO_CASE_ID_D'

        itinerary = Itinerary.objects.create()
        itinerary.add_case(FOO_CASE_ID_A)
        itinerary.add_case(FOO_CASE_ID_B)

        itinerary = Itinerary.objects.create()
        itinerary.add_case(FOO_CASE_ID_C)

        all_cases = [
            {'case_id': FOO_CASE_ID_A},
            {'case_id': FOO_CASE_ID_B},
            {'case_id': FOO_CASE_ID_C},
            {'case_id': FOO_CASE_ID_D},
        ]
        # Mock the results from the BWV query
        mock_get_cases_from_bwv.return_value = all_cases

        cases = Itinerary.get_unplanned_cases("2019-12-25", 'FOO_STADIUM')
        # Should only return the unplanned FOO_CASE_ID_D
        self.assertEquals(cases, [{'case_id': FOO_CASE_ID_D}])

    @freeze_time("2019-12-25")
    @patch('api.itinerary.models.get_cases_from_bwv')
    def test_get_unplanned_cases_empty(self, mock_get_cases_from_bwv):
        '''
        Should return all cases for another date
        '''
        FOO_CASE_ID_A = 'FOO_CASE_ID_A'
        FOO_CASE_ID_B = 'FOO_CASE_ID_B'
        FOO_CASE_ID_C = 'FOO_CASE_ID_C'
        FOO_CASE_ID_D = 'FOO_CASE_ID_D'

        itinerary = Itinerary.objects.create()
        itinerary.add_case(FOO_CASE_ID_A)
        itinerary.add_case(FOO_CASE_ID_B)

        itinerary = Itinerary.objects.create()
        itinerary.add_case(FOO_CASE_ID_C)

        all_cases = [
            {'case_id': FOO_CASE_ID_A},
            {'case_id': FOO_CASE_ID_B},
            {'case_id': FOO_CASE_ID_C},
            {'case_id': FOO_CASE_ID_D},
        ]
        # Mock the results from the BWV query
        mock_get_cases_from_bwv.return_value = all_cases

        cases = Itinerary.get_unplanned_cases("2018-01-01", 'FOO_STADIUM')
        self.assertEquals(cases, all_cases)

    def test_add_team_members(self):
        '''
        Adds team members to the given itinerary
        '''
        itinerary = Itinerary.objects.create()

        self.assertEquals([], list(itinerary.team_members.all()))

        user_a = User.objects.create(email='foo_a@foo.com')
        user_b = User.objects.create(email='foo_b@foo.com')
        itinerary.add_team_members([user_a.id, user_b.id])

        team_members = itinerary.team_members.all()
        team_member_users = [team_member.user for team_member in team_members]

        self.assertEquals([user_a, user_b], team_member_users)

    def test_clear_team_members(self):
        '''
        Removes all associated team members
        '''
        itinerary = Itinerary.objects.create()
        user_a = User.objects.create(email='foo_a@foo.com')
        user_b = User.objects.create(email='foo_b@foo.com')
        itinerary.add_team_members([user_a.id, user_b.id])

        team_members = itinerary.team_members.all()
        team_member_users = [team_member.user for team_member in team_members]
        self.assertEquals([user_a, user_b], team_member_users)

        itinerary.clear_team_members()
        self.assertEquals([], list(itinerary.team_members.all()))

    def test_get_center(self):
        '''
        Returns the center (average) of a list of cases
        '''
        itinerary = Itinerary.objects.create()

        mock_case_a = Mock()
        mock_case_b = Mock()

        mock_case_a.get_location = Mock(return_value={'lat': 1, 'lng': 1})
        mock_case_b.get_location = Mock(return_value={'lat': 2, 'lng': 2})

        mock_cases = [mock_case_a, mock_case_b]
        itinerary.get_cases = Mock(return_value=mock_cases)

        expected_center = {'lat': 1.5, 'lng': 1.5}
        center = itinerary.get_center()

        self.assertEqual(expected_center, center)

    def test_get_center_no_cases(self):
        '''
        Returns the city if no cases are present in the itinerary
        '''
        itinerary = Itinerary.objects.create()
        itinerary.get_cases = Mock(return_value=[])

        center = itinerary.get_center()
        city_center = itinerary.get_city_center()

        self.assertEqual(center, city_center)

    def test_get_city_center(self):
        '''
        Returns coordinates which are defined in the project's settings
        '''
        itinerary = Itinerary.objects.create()
        city_center = itinerary.get_city_center()

        self.assertEqual(city_center['lat'], settings.CITY_CENTRAL_LOCATION_LAT)
        self.assertEqual(city_center['lng'], settings.CITY_CENTRAL_LOCATION_LNG)

    @patch('api.itinerary.models.ItineraryKnapsackSuggestions')
    def test_get_suggestions(self, MockItineraryKnapsackSuggestions):
        '''
        Calls the ItineraryKnapsackSuggestions generate and exclude functions
        '''
        itinerary = Itinerary.objects.create()
        ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)

        itinerary.get_suggestions()
        MockItineraryKnapsackSuggestions().exclude.assert_called()
        MockItineraryKnapsackSuggestions().generate.assert_called()

    @patch('api.itinerary.models.ItineraryKnapsackList')
    def test_get_cases_from_settings(self, ItineraryKnapsackList):
        '''
        Calls the ItineraryKnapsackList generate and exclude functions
        '''
        itinerary = Itinerary.objects.create()
        ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)

        itinerary.get_cases_from_settings()
        ItineraryKnapsackList().exclude.assert_called()
        ItineraryKnapsackList().generate.assert_called()
