import logging
from api.cases.const import ISSUEMELDING
from api.planner.clustering import optics_clustering
from api.planner.utils import get_best_list
from api.planner.utils import sort_with_stadium
from api.planner.utils import shorten_if_necessary
from api.planner.algorithm.base import ItineraryGenerateAlgorithm

LOGGER = logging.getLogger(__name__)

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
