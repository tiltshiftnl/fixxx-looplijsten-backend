from api.cases import const
from enum import Enum

class SCORING_WEIGHTS(Enum):
    DISTANCE = 0.5
    FRAUD_PROBABILITY = 1
    PRIMARY_STADIUM = 0.75
    SECONDARY_STADIUM = 0.5
    ISSUEMELDING = 0.75


EXAMPLE_PLANNER_SETTINGS = {
    "opening_date": "2019-01-01",
    "projects": const.PROJECTS_WITHOUT_SAHARA,
    "lists": [
        {
            "name": "Maandag Ochtend",
            "length_of_lists": 6
        },
        {
            "name": "Maandag Middag",
            "length_of_lists": 6
        },
        {
            "name": "Maandag Avond",
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Dinsdag Ochtend",
            "length_of_lists": 6
        },
        {
            "name": "Dinsdag Middag",
            "length_of_lists": 6
        },
        {
            "name": "Dinsdag Avond",
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Woensdag Ochtend",
            "length_of_lists": 6
        },
        {
            "name": "Woensdag Middag",
            "length_of_lists": 6
        },
        {
            "name": "Woensdag Avond",
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Donderdag Ochtend",
            "number_of_lists": 2,
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Donderdag Middag",
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Donderdag Avond",
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Vrijdag Ochtend",
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Vrijdag Middag",
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Vrijdag Avond",
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Zaterdag Weekend",
            "length_of_lists": 12,
            "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Zondag Weekend",
            "length_of_lists": 12,
            "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        }
    ]
}
