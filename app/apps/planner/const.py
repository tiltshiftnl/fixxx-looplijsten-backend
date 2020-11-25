from enum import Enum

from apps.visits.models import Visit
from settings import const


# Note: currently the weights are defined as an Enum class.
# Eventually we might want to make this configurable through the settings page or admin
class SCORING_WEIGHTS(Enum):
    DISTANCE = 0.25
    FRAUD_PROBABILITY = 1
    PRIMARY_STADIUM = 0.25
    SECONDARY_STADIUM = 0.25
    ISSUEMELDING = 0.25
    IS_SIA = 1


MAX_SUGGESTIONS_COUNT = 20
