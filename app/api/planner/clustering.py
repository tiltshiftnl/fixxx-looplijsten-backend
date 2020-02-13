from sklearn.cluster import KMeans
import numpy as np

from api.planner.utils import sort_by_postal_code

def filter_cases_with_missing_coordinated(cases):
    def has_missing_coordinates(case):
        return case['lat'] is not None and case['lng']

    return list(filter(lambda case: has_missing_coordinates(case), cases))

def k_means_grouping(n_lists, cases):
    coordinates = list(map(lambda case: [case['lat'], case['lng']], cases))
    coordinates = np.array(coordinates)

    kmeans = KMeans(n_clusters=n_lists, random_state=0).fit(coordinates)

    print('K-MEANS HELLO WORLD')
    print(kmeans.labels_)
    # print(kmeans.predict([[0, 0], [12, 3]]))
    print(kmeans.cluster_centers_)


def postal_code_grouping(n_lists, cases, lengh_of_lists=8):
    """
    Plans lists bases on postal code
    """
    sorted_cases = sort_by_postal_code(cases)
    unplanned_cases = sorted_cases

    lists = []
    for i in range(0, n_lists):
        new_list = []
        for x in range(lengh_of_lists):
            if len(cases) == 0:
                break
            case = unplanned_cases.pop()
            new_list.append(case)
        lists.append(new_list)

    return lists, unplanned_cases
