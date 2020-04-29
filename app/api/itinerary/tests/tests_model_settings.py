from django.test import TestCase
from django.conf import settings
from api.itinerary.models import ItinerarySettings, Itinerary
from api.cases.models import Stadium, Project, Case

class ItinerarySettingsModelTest(TestCase):

    def get_new_itinerary_settings(self):
        '''
        Helper function to create basic new ItinerarySettings object
        '''
        itinerary = Itinerary.objects.create()
        return ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)

    def test_create_itinerary_settings(self):
        '''
        ItinerarySettings can be created
        '''
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        self.get_new_itinerary_settings()
        self.assertEquals(ItinerarySettings.objects.count(), 1)

    def test_target_length_default(self):
        '''
        Target length should default to 8
        '''
        itinerary_settings = self.get_new_itinerary_settings()
        self.assertEquals(8, itinerary_settings.target_length)

    def test_create_with_projects(self):
        '''
        Test adding projects through ManyToManyField
        '''
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        itinerary_settings = self.get_new_itinerary_settings()

        projects = [
            Project.get('FOO_PROJECT_A'),
            Project.get('FOO_PROJECT_B')
        ]
        itinerary_settings.projects.set(projects)
        itinerary_settings.save()
        self.assertEquals(itinerary_settings.projects.count(), 2)

    def test_create_with_primary_stadium(self):
        '''
        Test creating with primary_stadium
        '''
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        itinerary = Itinerary.objects.create()
        primary_stadium = Stadium.get('FOO_PRIMARY_STADIM')
        ItinerarySettings.objects.create(
            opening_date='2020-04-04',
            itinerary=itinerary,
            primary_stadium=primary_stadium
        )
        self.assertEquals(ItinerarySettings.objects.count(), 1)

    def test_create_with_secondary_stadia(self):
        '''
        Test adding secondary_stadia through ManyToManyField
        '''
        itinerary_settings = self.get_new_itinerary_settings()

        stadia = [
            Stadium.get('FOO_STADIUM_A'),
            Stadium.get('FOO_STADIUM_B')
        ]
        itinerary_settings.secondary_stadia.set(stadia)
        itinerary_settings.save()
        self.assertEquals(itinerary_settings.secondary_stadia.count(), 2)

    def test_create_with_exclude_stadia(self):
        '''
        Test adding exclude_stadia through ManyToManyField
        '''
        itinerary_settings = self.get_new_itinerary_settings()

        stadia = [
            Stadium.get('FOO_STADIUM_A'),
            Stadium.get('FOO_STADIUM_B')
        ]

        itinerary_settings.exclude_stadia.set(stadia)
        itinerary_settings.save()
        self.assertEquals(itinerary_settings.exclude_stadia.count(), 2)

    def test_create_with_start_case(self):
        '''
        Test creating with start_case
        '''
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        itinerary = Itinerary.objects.create()
        case = Case.get('FOO_CASE_ID')

        ItinerarySettings.objects.create(
            opening_date='2020-04-04',
            itinerary=itinerary,
            start_case=case
        )
        self.assertEquals(ItinerarySettings.objects.count(), 1)

    def test_with_postal_code_range(self):
        '''
        Test creating with postal code range
        '''
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE

        ItinerarySettings.objects.create(
            opening_date='2020-04-04',
            itinerary=itinerary,
            postal_code_range_start=FOO_MIN_RANGE,
            postal_code_range_end=FOO_MAX_RANGE
        )
        self.assertEquals(ItinerarySettings.objects.count(), 1)

    def test_with_postal_code_range_fail(self):
        '''
        Should fail if the range_start is larger than the range_end
        '''
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(
                opening_date='2020-04-04',
                itinerary=itinerary,
                postal_code_range_start=FOO_MAX_RANGE,
                postal_code_range_end=FOO_MIN_RANGE,
            )
            itinerary_settings.clean()

    def test_with_postal_code_range_fail_missing_range_end(self):
        '''
        Should fail if the range_end is missing
        '''
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(
                opening_date='2020-04-04',
                itinerary=itinerary,
                postal_code_range_start=FOO_MIN_RANGE
            )
            itinerary_settings.clean()

    def test_with_postal_code_range_fail_missing_range_start(self):
        '''
        Should fail if the range_end is missing
        '''
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(
                opening_date='2020-04-04',
                itinerary=itinerary,
                postal_code_range_end=FOO_MIN_RANGE
            )
            itinerary_settings.clean()
