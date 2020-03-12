from api.cases.const import STADIA
from api.planner.queries_planner import get_cases_from_bwv
from api.planner.clustering import optics_clustering
from api.planner.utils import filter_cases, get_best_list, remove_cases_from_list, sort_by_postal_code
from api.planner.utils import filter_cases_with_missing_coordinates, sort_with_stadium, filter_out_cases
from api.planner.utils import shorten_if_necessary, calculate_geo_distances

def get_cases_for_configuration(configuration):
    opening_date = configuration.get('opening_date')
    opening_reasons = configuration.get('opening_reasons')
    return get_cases_from_bwv(opening_date, opening_reasons, STADIA)

def get_list_for_planning(configuration):
    lists = configuration.get("lists", [])

    # Add incremental id's for list items
    for index, item in enumerate(lists):
        item['id'] = index

    # Now sort list based on availability of primary_stadium and secondary_stadia
    def get_sorting_priority(item):
        priority = 0
        primary_stadium = item.get('primary_stadium', False)
        secondary_stadia = item.get('secondary_stadia', [])

        if primary_stadium:
            priority += 1

        if len(secondary_stadia) > 0:
            priority += 1

        return priority

    lists.sort(key=get_sorting_priority)
    lists.reverse()

    return lists

def get_lists_in_original_order(lists):
    return sorted(lists, key=lambda case: case.get('id'))

def get_cases_with_settings(
        opening_date,
        target_length=8,
        projects=[],
        primary_stadium=None,
        secondary_stadia=[],
        exclude_stadia=[],
        exclude_cases=[]):

    cases = get_cases_from_bwv(opening_date, projects, STADIA)
    exclude_cases = [{'case_id': case.case_id} for case in exclude_cases]
    # TODO: this function can probably be written at a later point so that the previous mapping is not needed
    cases = remove_cases_from_list(cases, exclude_cases)

    itineraries = get_itineraries(
        cases=cases,
        number_of_lists=1,
        length_of_lists=target_length,
        primary_stadium=primary_stadium,
        secondary_stadia=secondary_stadia,
        exclude_stadia=exclude_stadia
    )

    return itineraries[0]


def get_planning(configuration):
    cases = get_cases_for_configuration(configuration)
    lists = get_list_for_planning(configuration)

    for item in lists:
        primary_stadium = item.get('primary_stadium', None)
        secondary_stadia = item.get('secondary_stadia', [])
        exclude_stadia = item.get('exclude_stadia', [])
        number_of_lists = item.get('number_of_lists', 0)
        length_of_lists = item.get('length_of_lists', 0)

        itineraries = get_itineraries(
            cases=cases,
            number_of_lists=number_of_lists,
            length_of_lists=length_of_lists,
            primary_stadium=primary_stadium,
            secondary_stadia=secondary_stadia,
            exclude_stadia=exclude_stadia
        )

        for itinerary in itineraries:
            cases = remove_cases_from_list(cases, itinerary)

        item['itineraries'] = itineraries

    lists = get_lists_in_original_order(lists)

    configuration['lists'] = lists
    configuration['unplanned_cases'] = sort_by_postal_code(cases)

    return configuration

# TODO: A lot of this code is repeated in get_itineraries. This is for prototype/demo purposes
def get_suggestions(
        center,
        opening_date,
        projects,
        primary_stadium=None,
        secondary_stadia=[],
        exclude_stadia=[],
        exclude_cases=[]):

    cases = get_cases_from_bwv(opening_date, projects, STADIA)

    exclude_cases = [{'case_id': case.case_id} for case in exclude_cases]
    # TODO: this function can probably be written at a later point so that the previous mapping is not needed
    cases = remove_cases_from_list(cases, exclude_cases)

    # Get a subset of cases containing the primary_stadium and secondary_stadia cases
    filter_stadia = secondary_stadia
    if primary_stadium:
        filter_stadia = [primary_stadium] + filter_stadia

    filtered_cases = filter_cases(cases, filter_stadia)
    filtered_cases = filter_out_cases(filtered_cases, exclude_stadia)
    filtered_cases = filter_cases_with_missing_coordinates(filtered_cases)

    # Calculate a list of distances for each case
    center = [center.get('lat'), center.get('lng')]
    distances = calculate_geo_distances(center, filtered_cases)

    # Add the distances to the cases
    for index, case in enumerate(filtered_cases):
        case['distance'] = distances[index]

    # Sort the cases based on distance
    sorted_cases = sorted(filtered_cases, key=lambda case: case['distance'])
    return sorted_cases

def get_itineraries(
        cases,
        number_of_lists,
        length_of_lists,
        primary_stadium=None,
        secondary_stadia=[],
        exclude_stadia=[]):
    itineraries = [[] for item in range(0, number_of_lists)]

    # Get a subset of cases containing the primary_stadium and secondary_stadia cases
    filter_stadia = secondary_stadia
    if primary_stadium:
        filter_stadia = [primary_stadium] + filter_stadia

    filtered_cases = filter_cases(cases, filter_stadia)
    filtered_cases = filter_out_cases(filtered_cases, exclude_stadia)
    filtered_cases = filter_cases_with_missing_coordinates(filtered_cases)

    # Copy the cases into a unplanned cases list
    unplanned_cases = filtered_cases.copy()

    for i in range(number_of_lists):
        # Break out of the loop if all cases have been planned
        if len(unplanned_cases) == 0:
            break

        # TODO: Refine these min fallbacks (also see MIN_SAMPLE_SIZE fallback in optics_clustering)
        # The cluster size cannot be larger then the number of unplanned cases
        cluster_size = min(length_of_lists, len(unplanned_cases))

        # Do a clustering using this subset
        clusters, rest = optics_clustering(cluster_size, unplanned_cases)

        # Select the best list and append it to the itinerary
        if len(clusters) > 0:

            best_list = get_best_list(clusters, primary_stadium)
            shortened_list = shorten_if_necessary(best_list, length_of_lists)
            sorted_best_list = sort_with_stadium(shortened_list, primary_stadium)

            itineraries[i] = sorted_best_list

            # remove the list from the unplanned cases
            unplanned_cases = remove_cases_from_list(unplanned_cases, itineraries[i])

    return itineraries
