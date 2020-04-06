import logging
from api.cases.const import STADIA, ISSUEMELDING
from utils.queries_planner import get_cases_from_bwv
from api.planner.utils import filter_cases, remove_cases_from_list
from api.planner.utils import filter_cases_with_missing_coordinates, filter_out_cases
from api.fraudprediction.models import FraudPrediction
from api.fraudprediction.serializers import FraudPredictionSerializer

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
            fraud_prediction_dictionary[fraud_prediction.case_id] = FraudPredictionSerializer(
                fraud_prediction).data

        return fraud_prediction_dictionary

    def exclude(self, cases):
        '''
        Makes sure the givens are not used when generating a list
        '''
        self.exclude_cases = cases

    def generate(self):
        raise NotImplementedError()
