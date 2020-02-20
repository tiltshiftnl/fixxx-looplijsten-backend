
from api.planner.const import STAGES
from api.planner.queries_planner import get_cases
from api.planner.clustering import optics_clustering
from api.planner.utils import filter_cases, get_best_list, remove_cases_from_list
from api.planner.utils import filter_cases_with_missing_coordinates, sort_with_stadium, filter_out_cases

def get_cases_for_configuration(configuration):
    opening_date = configuration.get('opening_date')
    opening_reasons = configuration.get('opening_reasons')
    return get_cases(opening_date, opening_reasons, STAGES)

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
    configuration['unplanned_cases'] = cases

    return configuration


def get_itineraries(cases, number_of_lists, length_of_lists, primary_stadium=None, secondary_stadia=[], exclude_stadia=[]):
    itineraries = []

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

        if len(clusters) > 0:
            # Select the best list and append it to the itinerary
            best_list = get_best_list(clusters, primary_stadium)
            sorted_best_list = sort_with_stadium(best_list, primary_stadium)
            shortened_list = sorted_best_list[:length_of_lists]

            itineraries.append(shortened_list)

            # remove the list from the unplanned cases
            unplanned_cases = remove_cases_from_list(unplanned_cases, shortened_list)

    return itineraries
