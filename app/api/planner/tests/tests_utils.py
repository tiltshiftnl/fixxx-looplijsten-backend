"""
Tests for the health views
"""
from django.test import TestCase
import numpy as np
from api.planner.utils import sort_by_postal_code, filter_cases, get_count, get_best_list
from api.planner.utils import remove_cases_from_list, get_case_coordinates, calculate_distances
from api.planner.utils import sort_with_stadium, filter_cases_with_missing_coordinates, filter_out_cases
from api.planner.utils import shorten_if_necessary
from api.planner.const import BED_AND_BREAKFAST, HOTLINE, SAFARI

# TODO: Split up in multiple classes
class UtilsTests(TestCase):
    def test_sort_by_postal_code(self):
        case_a = {'postal_code': '1088XX'}
        case_b = {'postal_code': '1077AA'}
        case_c = {'postal_code': '1076AA'}

        cases = [case_a, case_b, case_c]
        result = sort_by_postal_code(cases)
        expected = [case_c, case_b, case_a]

        self.assertEquals(result, expected)

    def test_filter_cases(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_cases(cases, [BED_AND_BREAKFAST, HOTLINE])
        expected = [case_a, case_b]

        self.assertEquals(result, expected)

    def test_filter_cases_empty(self):
        result = filter_cases([], [BED_AND_BREAKFAST, HOTLINE])
        self.assertEquals(result, [])

    def test_filter_cases_no_stadia(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_cases(cases, [])

        self.assertEquals(result, cases)

    def test_filter_cases_one_stadium(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_cases(cases, [SAFARI])
        expected = [case_c]

        self.assertEquals(result, expected)

    def test_get_count(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': BED_AND_BREAKFAST}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = get_count(cases, SAFARI)

        self.assertEquals(result, 1)

    def test_get_count_no_stadium(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': BED_AND_BREAKFAST}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = get_count(cases, None)

        self.assertEquals(result, 0)

    def test_get_count_multiple(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': BED_AND_BREAKFAST}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = get_count(cases, BED_AND_BREAKFAST)

        self.assertEquals(result, 2)

    def test_get_best_list(self):

        list_a = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE}]
        list_b = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST}]
        list_c = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': HOTLINE}]
        lists = [list_a, list_b, list_c]

        best_list = get_best_list(lists, BED_AND_BREAKFAST)
        self.assertEquals(best_list, list_b)

    def test_get_best_list_no_stadium(self):

        list_a = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE}]
        list_b = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST}]
        list_c = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': HOTLINE}]
        lists = [list_a, list_b, list_c]

        best_list = get_best_list(lists, None)
        # Will just return the first list if no Stadium if given
        self.assertEquals(best_list, list_a)

    def test_remove_cases_from_list(self):
        case_a = {'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-a'}
        case_b = {'stadium': HOTLINE, 'case_id': 'foo-b'}
        case_c = {'stadium': SAFARI, 'case_id': 'foo-c'}
        case_d = {'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-d'}
        case_e = {'stadium': HOTLINE, 'case_id': 'foo-e'}

        cases = [case_a, case_b, case_c, case_d, case_e]
        cases_to_remove = [case_b, case_e]

        result = remove_cases_from_list(cases, cases_to_remove)
        expected = [case_a, case_c, case_d]

        self.assertEquals(result, expected)

    def test_remove_cases_from_list_safety_fallback(self):
        '''
        Wil still succeed if tiems from the cases_to_remove don't exist in the cases list
        '''
        case_a = {'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-a'}
        case_b = {'stadium': HOTLINE, 'case_id': 'foo-b'}
        case_c = {'stadium': SAFARI, 'case_id': 'foo-c'}
        case_d = {'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-d'}
        case_e = {'stadium': HOTLINE, 'case_id': 'foo-e'}
        case_not_in_list = {'stadium': HOTLINE, 'case_id': 'foo-f'}

        cases = [case_a, case_b, case_c, case_d, case_e]
        cases_to_remove = [case_a, case_b, case_not_in_list]

        result = remove_cases_from_list(cases, cases_to_remove)
        expected = [case_c, case_d, case_e]

        self.assertEquals(result, expected)

    def test_get_case_coordinates(self):
        case_a = {'lat': 0, 'lng': 1, 'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-a'}
        case_b = {'lat': 2, 'lng': 3, 'stadium': HOTLINE, 'case_id': 'foo-b'}
        case_c = {'lat': 4, 'lng': 5, 'stadium': SAFARI, 'case_id': 'foo-c'}
        cases = [case_a, case_b, case_c]
        case_coordinates = get_case_coordinates(cases)
        expected = np.array([
            [0, 1],
            [2, 3],
            [4, 5]
        ])

        self.assertEquals(case_coordinates.all(), expected.all())

    def test_get_case_distances(self):
        case_a = {'lat': 0, 'lng': 1, 'stadium': BED_AND_BREAKFAST, 'case_id': 'foo-a'}
        case_b = {'lat': 0, 'lng': 2, 'stadium': HOTLINE, 'case_id': 'foo-b'}

        cases = [case_a, case_b]
        center = [0, 0]
        results = calculate_distances(center, cases)

        self.assertEquals(results, [1, 2])

        center = [0, 1]
        results = calculate_distances(center, cases)

        self.assertEquals(results, [0, 1])

    def sort_with_stadium(self):
        cases = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE}
        ]

        expected = [
            {'stadium': HOTLINE},
            {'stadium': HOTLINE},
            {'stadium': HOTLINE},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST}
        ]

        results = sort_with_stadium(cases, HOTLINE)

        self.assertEquals(expected, results)

    def sort_with_no_stadium(self):
        '''
        Should return the given list if no stadium is given
        '''
        cases = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE}
        ]

        results = sort_with_stadium(cases, None)

        self.assertEquals(cases, results)

    def test_filter_cases_with_missing_coordinates(self):
        '''
        Should filter out cases with missing coordinates
        '''
        valid_case = {'stadium': HOTLINE, 'lat': 12, 'lng': -69}
        cases = [
            {'stadium': BED_AND_BREAKFAST},
            {'stadium': HOTLINE, 'lat': 12},
            {'stadium': BED_AND_BREAKFAST, 'lng': -69},
            {'stadium': HOTLINE, 'lat': 12},
            {'stadium': HOTLINE, 'lat': None, 'lng': -69},
            {'stadium': BED_AND_BREAKFAST, 'lat': 12, 'lng': None},
            {'stadium': BED_AND_BREAKFAST, 'lat': None, 'lng': None},
            valid_case,
        ]

        filtered_cases = filter_cases_with_missing_coordinates(cases)
        self.assertEquals(filtered_cases, [valid_case])

    def test_filter_out_cases(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_out_cases(cases, [BED_AND_BREAKFAST, HOTLINE])
        expected = [case_c]

        self.assertEquals(result, expected)

    def test_filter_out_cases_empty(self):
        result = filter_out_cases([], [BED_AND_BREAKFAST, HOTLINE])
        self.assertEquals(result, [])

    def test_filter_out_cases_no_stadia(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_out_cases(cases, [])

        self.assertEquals(result, cases)

    def test_filter_out_cases_one_stadium(self):
        case_a = {'stadium': BED_AND_BREAKFAST}
        case_b = {'stadium': HOTLINE}
        case_c = {'stadium': SAFARI}

        cases = [case_a, case_b, case_c]
        result = filter_out_cases(cases, [SAFARI])
        expected = [case_a, case_b]

        self.assertEquals(result, expected)

    def test_shorten_if_necessary_normal(self):
        '''
        Does a normal shortening
        '''
        case_a = {'street_name': 'foo street A', 'street_number': 11}
        case_b = {'street_name': 'foo street B', 'street_number': 12}
        case_c = {'street_name': 'foo street C', 'street_number': 13}
        cases = [case_a, case_b, case_c]

        result = shorten_if_necessary(cases, 2)
        expected = [case_a, case_b]

        self.assertEquals(result, expected)

    def test_shorten_if_necessary_extra(self):
        '''
        Doesn't shorten because of grouped addresses
        '''
        case_a = {'street_name': 'foo street A', 'street_number': 11}
        case_b = {'street_name': 'foo street B', 'street_number': 12}
        case_c = {'street_name': 'foo street C', 'street_number': 13}
        cases = [case_c, case_a, case_b, case_c, case_c, case_c]

        result = shorten_if_necessary(cases, 3)
        expected = [case_a, case_b, case_c, case_c, case_c, case_c]

        self.assertEquals(result, expected)

    def test_shorten_if_necessary_multiple_extra(self):
        '''
        Doesn't shorten because of (multiple) grouped addresses
        '''
        case_a = {'street_name': 'foo street A', 'street_number': 11}
        case_b = {'street_name': 'foo street B', 'street_number': 12}
        case_c = {'street_name': 'foo street C', 'street_number': 13}
        cases = [case_c, case_a, case_b, case_a, case_c, case_c, case_c]

        result = shorten_if_necessary(cases, 6)
        expected = [case_a, case_a, case_b, case_c, case_c, case_c, case_c]

        self.assertEquals(result, expected)

    def test_shorten_if_necessary_exceeding_length(self):
        '''
        Doesn't shorten because length_target exceeds the list length
        '''
        case_a = {'street_name': 'foo street A', 'street_number': 11}
        case_b = {'street_name': 'foo street B', 'street_number': 12}
        case_c = {'street_name': 'foo street C', 'street_number': 13}
        cases = [case_c, case_a, case_b, case_c, case_c, case_c]

        result = shorten_if_necessary(cases, 8)
        expected = [case_a, case_b, case_c, case_c, case_c, case_c]

        self.assertEquals(result, expected)
