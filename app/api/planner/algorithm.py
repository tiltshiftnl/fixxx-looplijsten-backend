import multiprocessing
import logging
from time import process_time
from joblib import Parallel, delayed
from api.cases.const import STADIA, ISSUEMELDING
from utils.queries_planner import get_cases_from_bwv
from api.planner.clustering import optics_clustering
from api.planner.utils import filter_cases, get_best_list, remove_cases_from_list
from api.planner.utils import filter_cases_with_missing_coordinates, sort_with_stadium, filter_out_cases
from api.planner.utils import shorten_if_necessary, calculate_geo_distances
from api.fraudprediction.utils import get_fraud_prediction
from api.fraudprediction.models import FraudPrediction

LOGGER = logging.getLogger(__name__)

class ItineraryGenerateAlgorithm():
    ''' An abstract class which forms the basis of itinerary generating algorithms '''

    def __init__(self, settings):
        self.opening_date = settings.opening_date
        self.stadia = STADIA
        self.target_length = settings.target_length

        try:
            self.primary_stadium = settings.primary_stadium.name
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
        # Note: this might have to change at some point.
        # If not primary and secondary stadia are set, include all stadia
        if not self.primary_stadium and not self.secondary_stadia:
            return STADIA

        filter_stadia = self.secondary_stadia + [ISSUEMELDING]
        if self.primary_stadium:
            filter_stadia = filter_stadia + [self.primary_stadium]

        return filter_stadia

    def __get_eligible_cases__(self):
        '''
        Returns a list of eligible cases using the settings object
        '''
        cases = get_cases_from_bwv(self.opening_date, self.projects, self.stadia)
        LOGGER.info('Total list of cases: {}'.format(len(cases)))

        filter_stadia = self.__get_filter_stadia__()

        LOGGER.info('Filter stadia: {}'.format(str(filter_stadia)))
        LOGGER.info('Exclude stadia: {}'.format(str(self.exclude_stadia)))
        LOGGER.info('Projects: {}'.format(str(self.projects)))
        LOGGER.info('Opening date: {}'.format(str(self.opening_date)))

        filtered_cases = filter_cases(cases, filter_stadia)
        LOGGER.info('Total cases after filtering stadia: {}'.format(len(filtered_cases)))

        filtered_cases = filter_out_cases(filtered_cases, self.exclude_stadia)
        LOGGER.info('Total cases after excluding stadia: {}'.format(len(filtered_cases)))

        filtered_cases = filter_cases_with_missing_coordinates(filtered_cases)
        LOGGER.info('Total cases after filtering on missing coordinates: {}'.format(len(filtered_cases)))

        exclude_cases = [{'case_id': case.case_id} for case in self.exclude_cases]
        filtered_cases = remove_cases_from_list(filtered_cases, exclude_cases)
        LOGGER.info('Total cases after removing exclude cases: {}'.format(len(filtered_cases)))

        if not filter_cases:
            LOGGER.warning('No eligible cases found')
            raise ValueError('No eligible cases found')

        return filtered_cases

    def __get_fraud_predictions__(self):
        '''
        Returns a dictionary of fraud probabilities mapped to case_ids
        '''
        fraud_predictions = FraudPrediction.objects.all()
        fraud_prediction_dictionary = {}

        for fraud_prediction in fraud_predictions:
            fraud_prediction_dictionary[fraud_prediction.case_id] = fraud_prediction

        return fraud_prediction_dictionary

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

        LOGGER.info('Generating list with {} eligible cases'.format(len(cases)))

        # The cluster size cannot be larger then the number of unplanned cases
        cluster_size = min(self.target_length, len(cases))

        # Do a clustering using this subset
        clusters, rest = optics_clustering(cluster_size, cases)

        # Select the best list and append it to the itinerary
        if not clusters:
            LOGGER.warning('Could not generate clusters')
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
    def __init__(self, settings, settings_weights=None):
        super().__init__(settings)

        if settings_weights:
            self.weights = ItineraryKnapsackSuggestions.Weights(
                distance=settings_weights.distance,
                fraud_probability=settings_weights.fraud_probability,
                primary_stadium=settings_weights.primary_stadium,
                secondary_stadium=settings_weights.secondary_stadium,
                issuemelding=settings_weights.issuemelding
            )
        else:
            self.weights = ItineraryKnapsackSuggestions.Weights()

    class Weights():
        '''
        A configurable weight object which is used in our scoring function
        '''

        def __init__(self,
                     distance=2.5,
                     fraud_probability=2,
                     primary_stadium=2.5,
                     secondary_stadium=1,
                     issuemelding=2.5):

            self.distance = distance
            self.fraud_probability = fraud_probability
            self.primary_stadium = primary_stadium
            self.secondary_stadium = secondary_stadium
            self.issuemelding = issuemelding

        def score(
                self,
                distance,
                fraud_probability,
                primary_stadium,
                secondary_stadium,
                issuemelding):

            # TODO: improve readability of this
            return distance*self.distance + fraud_probability*self.fraud_probability + primary_stadium*self.primary_stadium + secondary_stadium*self.secondary_stadium + issuemelding*self.issuemelding

        def __str__(self):
            settings = {
                'distance': self.distance,
                'fraud_probability': self.fraud_probability,
                'primary_stadium': self.primary_stadium,
                'secondary_stadium': self.secondary_stadium,
                'issuemelding': self.issuemelding
            }
            return str(settings)

    def get_score(
            self,
            distance,
            fraud_probability,
            has_primary_stadium,
            has_secondary_stadium,
            has_issuemelding):
        '''
        Gets the score of our case
        '''
        score = self.weights.score(distance, fraud_probability, has_primary_stadium,
                                   has_secondary_stadium, has_secondary_stadium)
        return score

    def generate(self, location, cases=[], fraud_predictions=[]):
        if not cases:
            cases = self.__get_eligible_cases__()

        if not fraud_predictions:
            fraud_predictions = self.__get_fraud_predictions__()

        # Calculate a list of distances for each case
        center = (location['lat'], location['lng'])
        distances = calculate_geo_distances(center, cases)
        max_distance = max(distances)

        # Add the distances and fraud predictions to the cases
        for index, case in enumerate(cases):
            case_id = case['case_id']
            stadium = case['stadium']

            distance = distances[index]
            normalized_inverse_distance = (max_distance - distance) / max_distance

            try:
                fraud_probability = fraud_predictions[case_id].fraud_probability
            except Exception:
                LOGGER.warning('Fraud probability does not exist: {}'.format(case_id))
                fraud_probability = 0

            has_primary_stadium = stadium == self.primary_stadium
            has_secondary_stadium = stadium in self.secondary_stadia
            has_issuemelding_stadium = stadium == ISSUEMELDING

            score = self.get_score(
                normalized_inverse_distance,
                fraud_probability,
                has_primary_stadium,
                has_secondary_stadium,
                has_issuemelding_stadium)

            # Store in case dictionary
            case['distance'] = distance
            case['fraud_prediction'] = fraud_probability
            case['score'] = score

        # Sort the cases based on score
        sorted_cases = sorted(cases, key=lambda case: case['score'], reverse=True)

        return sorted_cases


class ItineraryKnapsackList(ItineraryKnapsackSuggestions):

    def score_list(self, cases):
        scores = [case['score'] for case in cases]
        return sum(scores)

    def shorten_list(self, list):
        '''
        Shortens the list to target_length
        '''
        # Make sure the list is sorted on distance first
        return list[:self.target_length]

    def get_best_list(self, candidates):
        best_list = max(candidates, key=lambda candidate: candidate['score'])

        return best_list['list']

    def parallelized_function(self, case, cases, fraud_predictions, index):
        suggestions = super().generate(case, cases, fraud_predictions)
        suggestions = self.shorten_list(suggestions)
        score = self.score_list(suggestions)

        return {'score': score, 'list': suggestions}

    def generate(self, location=None):
        t = process_time()
        # For a location, just get the suggestions
        if location:
            suggestions = super().generate(location)
            return self.shorten_list(suggestions)

        # No location is given, so choose the optimial list on all possible
        # starting locations
        cases = self.__get_eligible_cases__()
        fraud_predictions = self.__get_fraud_predictions__()

        jobs = multiprocessing.cpu_count()
        candidates = Parallel(n_jobs=jobs, backend='multiprocessing')(delayed(self.parallelized_function)(
            case, cases, fraud_predictions, index) for index, case in enumerate(cases))

        best_list = self.get_best_list(candidates)
        best_list = sorted(best_list, key=lambda case: case['distance'])

        LOGGER.info('DONE {}'.format(process_time() - t))
        LOGGER.info('With {} cpus'.format(jobs))

        return best_list
