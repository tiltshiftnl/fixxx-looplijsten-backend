from api.cases.const import STADIA, ISSUEMELDING
from utils.queries_planner import get_cases_from_bwv
from api.planner.clustering import optics_clustering
from api.planner.utils import filter_cases, get_best_list, remove_cases_from_list
from api.planner.utils import filter_cases_with_missing_coordinates, sort_with_stadium, filter_out_cases
from api.planner.utils import shorten_if_necessary, calculate_geo_distances
from api.fraudprediction.utils import get_fraud_prediction

class ItineraryGenerateAlgorithm():
    ''' An abstract class which forms the basis of itinerary generating algorithms '''

    def __init__(self, settings):
        self.opening_date = settings.opening_date
        self.stadia = STADIA
        self.target_length = settings.target_length

        try:
            self.primary_stadium = settings.primary_stadium
        except AttributeError:
            self.primary_stadium = None

        self.projects = [project.name for project in settings.projects.all()]
        self.secondary_stadia = [stadium.name for stadium in settings.secondary_stadia.all()]
        self.exclude_stadia = [stadium.name for stadium in settings.exclude_stadia.all()]
        self.exclude_cases = []

    def __get_filter_stadia__(self):
        '''
        Gets a list of filter stadia
        '''
        filter_stadia = self.secondary_stadia
        if self.primary_stadium:
            filter_stadia = [self.primary_stadium, ISSUEMELDING] + filter_stadia

        return filter_stadia

    def __get_eligible_cases__(self):
        '''
        Returns a list of eligible cases using the settings object
        '''
        cases = get_cases_from_bwv(self.opening_date, self.projects, self.stadia)
        filter_stadia = self.__get_filter_stadia__()

        filtered_cases = filter_cases(cases, filter_stadia)
        filtered_cases = filter_out_cases(filtered_cases, self.exclude_stadia)
        filtered_cases = filter_cases_with_missing_coordinates(filtered_cases)

        exclude_cases = [{'case_id': case.case_id} for case in self.exclude_cases]
        filtered_cases = remove_cases_from_list(filtered_cases, exclude_cases)

        return filtered_cases

    def exclude(self, cases):
        '''
        Makes sure the givens are not used when generating a list
        '''
        self.exclude_cases = cases

    def generate(self):
        raise NotImplementedError()


class ItineraryGenerateCluster(ItineraryGenerateAlgorithm):
    '''Generates an itinerary using a clustering algorithm'''

    def generate(self):
        cases = self.__get_eligible_cases__()

        if not cases:
            return []

        # The cluster size cannot be larger then the number of unplanned cases
        cluster_size = min(self.target_length, len(cases))

        # Do a clustering using this subset
        clusters, rest = optics_clustering(cluster_size, cases)

        # Select the best list and append it to the itinerary
        if not clusters:
            return []

        # Get the best list, shorten it, and sort it by primary stadium
        best_list = get_best_list(clusters, [self.primary_stadium, ISSUEMELDING])
        shortened_list = shorten_if_necessary(best_list, self.target_length)

        sorted_best_list = sort_with_stadium(shortened_list, self.primary_stadium)
        sorted_best_list = sort_with_stadium(sorted_best_list, ISSUEMELDING)

        return sorted_best_list


class ItineraryGenerateSuggestions(ItineraryGenerateAlgorithm):
    ''' Generates a list of suggestion based on a given location '''

    def generate(self, location):

        cases = self.__get_eligible_cases__()

        if not cases:
            return []

        # Calculate a list of distances for each case
        center = (location['lat'], location['lng'])
        distances = calculate_geo_distances(center, cases)

        # Add the distances and fraud predictions to the cases
        for index, case in enumerate(cases):
            case['distance'] = distances[index]
            case['fraud_prediction'] = get_fraud_prediction(case['case_id'])

        # Sort the cases based on distance
        sorted_cases = sorted(cases, key=lambda case: case['distance'])
        return sorted_cases


class ItineraryKnapsackSuggestions(ItineraryGenerateAlgorithm):

    class Weights():
        '''
        A configurable weight object which is used in our scoring function
        '''

        def __init__(self,
                     distance=1,
                     fraud_prediction=1,
                     primary_stadium=1,
                     secondary_stadium=0.5,
                     issuemelding=1):

            self.distance = distance
            self.fraud_prediction = fraud_prediction
            self.primary_stadium = primary_stadium
            self.secondary_stadium = secondary_stadium
            self.issuemelding = issuemelding

    def get_score(self, case):
        '''
        Gets the score of our case
        '''
        weights = ItineraryKnapsackSuggestions.Weights()
        key_weights = [
            ('normalized_inverse_distance', weights.distance),
            ('fraud_probability', weights.fraud_prediction),
            ('has_primary_stadium', weights.primary_stadium),
            ('has_secondary_stadium', weights.secondary_stadium),
            ('has_issuemelding_stadium', weights.issuemelding)
        ]
        scores = {}

        for key, weight in key_weights:
            print(key)
            print(weight)
            print(case[key])
            scores[key] = case[key] * weight

        scores['total_score'] = sum(scores.values())

        return scores

    def generate(self, location):
        cases = self.__get_eligible_cases__()

        if not cases:
            return []

        # Calculate a list of distances for each case
        center = (location['lat'], location['lng'])
        distances = calculate_geo_distances(center, cases)
        max_distance = max(distances)

        # Add the distances and fraud predictions to the cases
        for index, case in enumerate(cases):
            case['distance'] = distances[index]
            case['normalized_inverse_distance'] = (max_distance - case['distance']) / max_distance
            case['fraud_prediction'] = get_fraud_prediction(case['case_id'])
            case['fraud_probability'] = get_fraud_prediction(case['case_id'])['fraud_probability']
            case['has_primary_stadium'] = case['stadium'] == self.primary_stadium
            case['has_secondary_stadium'] = case['stadium'] in self.secondary_stadia
            case['has_issuemelding_stadium'] = case['stadium'] == ISSUEMELDING
            case['score'] = self.get_score(case)

        # Sort the cases based on score
        sorted_cases = sorted(cases, key=lambda case: case['score']['total_score'])
        sorted_cases.reverse()

        return sorted_cases
