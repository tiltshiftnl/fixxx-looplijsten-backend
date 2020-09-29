from enum import Enum

from apps.cases import const
from apps.visits import const as visits_const


class SCORING_WEIGHTS(Enum):
    DISTANCE = 1
    FRAUD_PROBABILITY = 1
    PRIMARY_STADIUM = 0.75
    SECONDARY_STADIUM = 0.5
    ISSUEMELDING = 0.75


MAX_SUGGESTIONS_COUNT = 20

EXAMPLE_PLANNER_SETTINGS = {
    "opening_date": "2019-01-01",
    "projects": const.PROJECTS_WITHOUT_SAHARA,
    # Optional postal code settings
    "postal_codes": [{"range_start": 1000, "range_end": 1109}],
    "days": {
        "monday": {
            "day": {
                "length_of_list": 6,
                "primary_stadium": const.ONDERZOEK_BUITENDIENST,
                "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE],
            },
            "evening": {
                "length_of_list": 6,
                "primary_stadium": const.AVONDRONDE,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            },
        },
        "tuesday": {
            "day": {},
            "evening": {
                "length_of_list": 6,
                "primary_stadium": const.AVONDRONDE,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            },
        },
        "wednesday": {
            "day": {},
            "evening": {
                "length_of_list": 6,
                "primary_stadium": const.AVONDRONDE,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            },
        },
        "thursday": {
            "day": {
                "length_of_list": 6,
                "primary_stadium": const.ONDERZOEK_BUITENDIENST,
                "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE],
            },
            "evening": {
                "length_of_list": 6,
                "primary_stadium": const.AVONDRONDE,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            },
        },
        "friday": {
            "day": {
                "length_of_list": 6,
                "primary_stadium": const.ONDERZOEK_BUITENDIENST,
                "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE],
            },
            "evening": {
                "length_of_list": 6,
                "primary_stadium": const.AVONDRONDE,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            },
        },
        "saturday": {
            "day": {
                "length_of_list": 6,
                "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            }
        },
        "sunday": {
            "day": {
                "length_of_list": 6,
                "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
                "secondary_stadia": [
                    const.HERCONTROLE,
                    const.TWEEDE_HERCONTROLE,
                    const.DERDE_HERCONTROLE,
                ],
            }
        },
    },
}

TEAM_TYPE_VAKANTIEVERHUUR = 'Vakantieverhuur'
TEAM_TYPE_ONDERVERHUUR = 'Onderverhuur'

TEAM_TYPE_SETTINGS = {
    TEAM_TYPE_VAKANTIEVERHUUR: {
        'name': TEAM_TYPE_VAKANTIEVERHUUR,
        'project_choices': const.PROJECTS_VAKANTIEVERHUUR,
        'stadia_choices': const.STADIA_VAKANTIEVERHUUR,
        'observation_choices': visits_const.OBSERVATIONS,
        'suggest_next_visit_choices': visits_const.SUGGEST_NEXT_VISIT,
        'situation_choices': visits_const.SITUATIONS,
        'week_day_choices': [0, 1, 2, 3, 4, 5, 6],
        'show_list_fraudprediction': True,
        'show_fraudprediction': True,
        'show_issuemelding': True,
    },
    TEAM_TYPE_ONDERVERHUUR: {
        'name': TEAM_TYPE_ONDERVERHUUR,
        'project_choices': const.PROJECTS_ONDERVERHUUR,
        'stadia_choices': const.STADIA_ONDERVERHUUR,
        'observation_choices': visits_const.OBSERVATIONS,
        'suggest_next_visit_choices': visits_const.SUGGEST_NEXT_VISIT,
        'situation_choices': visits_const.SITUATIONS,
        'week_day_choices': [0, 1, 2, 3, 4],
        'show_list_fraudprediction': False,
        'show_fraudprediction': False,
        'show_issuemelding': False,
    }
}

TEAM_TYPE_CHOICES = [[k, k] for k, v in TEAM_TYPE_SETTINGS.items()]
