from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

def sort_by_postal_code(cases):
    '''
    Sorts cases based on their postal_code
    '''
    return sorted(cases, key=lambda case: case.get('postal_code'))

# TODO: Test this
def filter_out_cases(cases, stadia):
    '''
    Returns a list of cases without the given stadia
    '''
    if len(stadia) == 0:
        return cases

    def has_stadium(case):
        return case['stadium'] not in stadia

    return list(filter(lambda case: has_stadium(case), cases))

def filter_cases(cases, stadia):
    '''
    Returns a list of cases with the given stadia
    '''
    if len(stadia) == 0:
        return cases

    def has_stadium(case):
        return case['stadium'] in stadia

    return list(filter(lambda case: has_stadium(case), cases))


def get_count(cases, stadium):
    '''
    Returns how many of the given cases have the given stadium
    '''
    cases_with_stadium = [case['stadium'] == stadium for case in cases]
    count = sum(cases_with_stadium)

    return count


def get_best_list(case_lists, primary_stadium):
    '''
    Returns the 'best' list, which is the list with most cases with the primary_stadium
    '''
    cases_counted = [get_count(case_list, primary_stadium) for case_list in case_lists]
    best_list_index = cases_counted.index(max(cases_counted))
    best_list = case_lists[best_list_index]

    return best_list

def sort_with_stadium(cases, stadium):
    '''
    Returns lists of cases in which the case is sorted by stadium
    '''
    # Just return the list as is if no stadium is given
    if stadium is None:
        return cases

    sorted_cases = sorted(cases, key=lambda case: case.get('stadium') == stadium)
    sorted_cases.reverse()

    return sorted_cases

def remove_cases_from_list(cases, cases_to_remove):
    '''
    Returns a new list without the 'cases_to_remove' items
    '''
    def should_not_remove(case):
        return case not in cases_to_remove

    new_list = list(filter(lambda case: should_not_remove(case), cases))

    return new_list


def get_case_coordinates(cases):
    '''
    Maps the cases to an array of coordinates
    '''
    coordinates = list(map(lambda case: [case['lat'], case['lng']], cases))

    return np.array(coordinates)


def calculate_distances(center, cases):
    '''
    Returns a set of (euclidean) distances from the given center
    '''
    case_coordinates = get_case_coordinates(cases)
    distances = euclidean_distances(case_coordinates, [center])

    return list(distances.flatten())

# TODO: Write test for this
def filter_cases_with_missing_coordinates(cases):
    def has_missing_coordinates(case):
        return case['lat'] is not None and case['lng']

    return list(filter(lambda case: has_missing_coordinates(case), cases))
