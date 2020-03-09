from api.cases import const

STARTING_DATE = "2019-01-01 00:00:00"

EXAMPLE_PLANNER_SETTINGS = {
    "opening_date": "2019-01-01",
    "opening_reasons": const.PROJECTS_WITHOUT_SAHARA,
    "lists": [
        {
            "name": "Maandag Ochtend",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Maandag Middag",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Maandag Avond",
            "number_of_lists": 0,
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Dinsdag Ochtend",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Dinsdag Middag",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Dinsdag Avond",
            "number_of_lists": 0,
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Woensdag Ochtend",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Woensdag Middag",
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "name": "Woensdag Avond",
            "number_of_lists": 0,
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
            "number_of_lists": 2,
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Donderdag Avond",
            "number_of_lists": 1,
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Vrijdag Ochtend",
            "number_of_lists": 2,
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Vrijdag Middag",
            "number_of_lists": 2,
            "length_of_lists": 6,
            "primary_stadium": const.ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [const.TWEEDE_CONTROLE, const.DERDE_CONTROLE]
        },
        {
            "name": "Vrijdag Avond",
            "number_of_lists": 0,
            "length_of_lists": 6,
            "primary_stadium": const.AVONDRONDE,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Zaterdag Weekend",
            "number_of_lists": 1,
            "length_of_lists": 12,
            "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        },
        {
            "name": "Zondag Weekend",
            "number_of_lists": 1,
            "length_of_lists": 12,
            "primary_stadium": const.WEEKEND_BUITENDIENST_ONDERZOEK,
            "secondary_stadia": [const.HERCONTROLE, const.TWEEDE_HERCONTROLE, const.DERDE_HERCONTROLE]
        }
    ]
}
