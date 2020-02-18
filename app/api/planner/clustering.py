from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS
from api.planner.utils import sort_by_postal_code, get_case_coordinates

def filter_cases_with_missing_coordinates(cases):
    def has_missing_coordinates(case):
        return case['lat'] is not None and case['lng']

    return list(filter(lambda case: has_missing_coordinates(case), cases))

def optics_grouping(cluster_size, cases):
    coordinates = get_case_coordinates(cases)
    clusters = OPTICS(min_samples=3, min_cluster_size=cluster_size).fit(coordinates)

    grouping_labels = clusters.labels_
    n_lists = max(grouping_labels) + 1

    groups = [[] for i in range(0, n_lists)]
    unplanned_cases = []

    for i in range(0, len(cases)):
        group = grouping_labels[i]
        case = cases[i]
        if group == -1:
            unplanned_cases.append(case)
        else:
            groups[group].append(case)

    return groups, unplanned_cases


def k_means_grouping(n_lists, cases):
    coordinates = get_case_coordinates(cases)
    clusters = KMeans(n_clusters=n_lists, random_state=0).fit(coordinates)
    grouping_labels = clusters.labels_

    groups = [[] for i in range(0, n_lists)]
    for i in range(0, len(cases)):
        group = grouping_labels[i]
        case = cases[i]
        groups[group].append(case)

    return groups


def postal_code_grouping(n_lists, cases, lengh_of_lists=8):
    """
    Plans lists bases on postal code
    """
    sorted_cases = sort_by_postal_code(cases)
    sorted_cases.reverse()
    unplanned_cases = sorted_cases.copy()

    lists = []
    for i in range(0, n_lists):
        new_list = []
        for x in range(lengh_of_lists):
            if len(unplanned_cases) == 0:
                break
            case = unplanned_cases.pop()
            new_list.append(case)
        lists.append(new_list)

    return lists, unplanned_cases
