from geopy.distance import distance

def filter_out_cases(cases, stadia=[]):
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

def remove_cases_from_list(cases, cases_to_remove):
    '''
    Returns a new list without the 'cases_to_remove' items
    '''
    cases_to_remove = [case.get('case_id') for case in cases_to_remove]

    def should_not_remove(case):
        return case.get('case_id') not in cases_to_remove

    new_list = list(filter(lambda case: should_not_remove(case), cases))

    return new_list

def get_case_coordinates(cases):
    '''
    Maps the cases to an array of coordinates
    '''
    coordinates = list(map(lambda case: [case['lat'], case['lng']], cases))

    return coordinates

def calculate_geo_distances(center, cases):
    '''
    Returns a set of distances in KM from the given center
    '''
    case_coordinates = get_case_coordinates(cases)
    distances = [distance(center, coordinates).km * 1000 for coordinates in case_coordinates]

    return distances


def filter_cases_with_missing_coordinates(cases):
    '''
    Cases with polluted data (missing coordinates) are removed
    '''
    def has_missing_coordinates(case):
        return case.get('lat') is not None and case.get('lng')

    return list(filter(lambda case: has_missing_coordinates(case), cases))
