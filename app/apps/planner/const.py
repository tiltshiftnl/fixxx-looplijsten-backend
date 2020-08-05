from enum import Enum

from apps.cases import const


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
