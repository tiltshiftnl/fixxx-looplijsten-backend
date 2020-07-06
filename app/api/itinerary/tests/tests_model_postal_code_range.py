from django.conf import settings
from django.test import TestCase

from api.itinerary.models import ItinerarySettings, Itinerary, PostalCodeRange

# Test reverse access

class ItinerarySettingsModelTest(TestCase):

    def test_with_postal_code_range(self):
        """
        Test creating with postal code range
        """
        self.assertEquals(ItinerarySettings.objects.count(), 0)
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE

        itinerary_settings = ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)
        postal_code_range = PostalCodeRange.objects.create(
            itinerary_settings=itinerary_settings,
            postal_code_range_start=FOO_MIN_RANGE,
            postal_code_range_end=FOO_MAX_RANGE
        )
        postal_code_range.clean()
        self.assertEquals(ItinerarySettings.objects.count(), 1)

    def test_with_postal_code_range_fail(self):
        """
        Should fail if the range_start is larger than the range_end
        """
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)
            postal_code_range = PostalCodeRange.objects.create(
                itinerary_settings=itinerary_settings,
                postal_code_range_start=FOO_MAX_RANGE,
                postal_code_range_end=FOO_MIN_RANGE
            )
            postal_code_range.clean()

    def test_with_postal_code_range_fail_missing_range_end(self):
        """
        Should fail if the range_end is missing
        """
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)
            postal_code_range = PostalCodeRange.objects.create(
                itinerary_settings=itinerary_settings,
                postal_code_range_start=FOO_MIN_RANGE,
            )
            postal_code_range.clean()

    def test_with_postal_code_range_fail_missing_range_start(self):
        """
        Should fail if the range_end is missing
        """
        itinerary = Itinerary.objects.create()
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE

        with self.assertRaises(Exception):
            itinerary_settings = ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)
            postal_code_range = PostalCodeRange.objects.create(
                itinerary_settings=itinerary_settings,
                postal_code_range_end=FOO_MAX_RANGE,
            )
            postal_code_range.clean()

    def test_reverse_access(self):
        """
        Multiple postal code ranges should be accessible through the ItinerarySettings object
        """
        itinerary = Itinerary.objects.create()
        FOO_MIN_RANGE = settings.CITY_MIN_POSTAL_CODE
        FOO_MAX_RANGE = settings.CITY_MAX_POSTAL_CODE
        N_RANGES = 4

        itinerary_settings = ItinerarySettings.objects.create(opening_date='2020-04-04', itinerary=itinerary)

        for i in range(N_RANGES):
            postal_code_range = PostalCodeRange.objects.create(
                itinerary_settings=itinerary_settings,
                postal_code_range_start=FOO_MIN_RANGE,
                postal_code_range_end=FOO_MAX_RANGE
            )
            postal_code_range.clean()

        self.assertEqual(itinerary_settings.postal_code_ranges.count(), N_RANGES+1)