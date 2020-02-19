STARTING_DATE = "2019-01-01 00:00:00"


BED_AND_BREAKFAST = "Bed en breakfast 2019"
BURGWALLEN_PROJECT_OUDEZIJDE = "Burgwallenproject Oudezijde"
CORPO_RICO = "Corpo-rico"
DIGITAAL_TOEZICHT_SAFARI = "Digital toezicht Safari"
DIGITAAL_TOEZICHT_ZEBRA = "Digital toezicht Zebra"
HAARLEMMERBUURT = "Haarlemmerbuurt"
HOTLINE = "Hotline"
MYSTERY_GUEST = "Mystery Guest"
PROJECT_ANDES = "Project Andes"
PROJECT_JORDAAN = "Project Jordaan"
PROJECT_LOBITH = "Project Lobith"
PROJECT_SAHARA = "Project Sahara"
SAFARI = "Safari"
PROJECT_SAFARI_2015 = "Safari 2015"
SAHARA_ADAMS_SUITES = "Sahara Adams Suites"
SAHARA_HELE_WONING = "Sahara hele woning"
SAHARA_MEER_DAN_4 = "Sahara meer dan 4"
SAHARA_RECENSIES = "Sahara Recensies"
SAHARA_VEEL_ADV = "Sahara veel adv"
PROJECT_SOCIAL_MEDIA_2019 = "Social Media 2019"
PROJECT_WOONSCHIP = "Woonschip (woonboot)"
PROJECT_ZEBRA = "Zebra"

PROJECTS = [
    BED_AND_BREAKFAST,
    BURGWALLEN_PROJECT_OUDEZIJDE,
    CORPO_RICO,
    DIGITAAL_TOEZICHT_SAFARI,
    DIGITAAL_TOEZICHT_ZEBRA,
    HAARLEMMERBUURT,
    HOTLINE,
    MYSTERY_GUEST,
    PROJECT_ANDES,
    PROJECT_JORDAAN,
    PROJECT_LOBITH,
    PROJECT_SAHARA,
    SAFARI,
    PROJECT_SAFARI_2015,
    SAHARA_ADAMS_SUITES,
    SAHARA_HELE_WONING,
    SAHARA_MEER_DAN_4,
    SAHARA_RECENSIES,
    SAHARA_VEEL_ADV,
    PROJECT_SOCIAL_MEDIA_2019,
    PROJECT_WOONSCHIP,
    PROJECT_ZEBRA,
]

PROJECTS_WITHOUT_SAHARA = [
    BED_AND_BREAKFAST,
    BURGWALLEN_PROJECT_OUDEZIJDE,
    CORPO_RICO,
    DIGITAAL_TOEZICHT_SAFARI,
    DIGITAAL_TOEZICHT_ZEBRA,
    HAARLEMMERBUURT,
    HOTLINE,
    MYSTERY_GUEST,
    PROJECT_ANDES,
    PROJECT_JORDAAN,
    PROJECT_LOBITH,
    SAFARI,
    PROJECT_SAFARI_2015,
    PROJECT_SOCIAL_MEDIA_2019,
    PROJECT_WOONSCHIP,
    PROJECT_ZEBRA,
]

# NOTE: More stages exist, such as the 'Issuemeldingen' which are currently not user
# By this application
TWEEDE_CONTROLE = "2de Controle"
TWEEDE_HERCONTROLE = "2de hercontrole"
DERDE_CONTROLE = "3de Controle"
DERDE_HERCONTROLE = "3de hercontrole"
AVONDRONDE = "Avondronde"
HERCONTROLE = "Hercontrole"
ONDERZOEK_ADVERDENTIE = "Onderzoek advertentie"
ONDERZOEK_BUITENDIENST = "Onderzoek buitendienst"
WEEKEND_BUITENDIENST_ONDERZOEK = "Weekend buitendienstonderzoek"

STAGES = [
    TWEEDE_CONTROLE,
    TWEEDE_HERCONTROLE,
    DERDE_CONTROLE,
    DERDE_HERCONTROLE,
    AVONDRONDE,
    HERCONTROLE,
    ONDERZOEK_ADVERDENTIE,
    ONDERZOEK_BUITENDIENST,
    WEEKEND_BUITENDIENST_ONDERZOEK,
]

EXAMPLE_POST = {
    "opening_date": "2018-01-01",
    "opening_reasons": [
        "Zebra",
        "Woonschip (woonboot)",
        "Social Media 2019",
        "Safari 2015",
        "Safari",
        "Project Lobith",
        "Project Jordaan",
        "Project Andes",
        "Mystery Guest",
        "Hotline",
        "Haarlemmerbuurt",
        "Digital toezicht Zebra",
        "Digital toezicht Safari",
        "Corpo-rico",
        "Burgwallenproject Oudezijde",
        "Bed en breakfast 2019"
    ],
    "lists": [
        {
            "number_of_lists": 2,
            "length_of_lists": 6
        },
        {
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "number_of_lists": 1,
            "length_of_lists": 6
        },
        {
            "number_of_lists": 2,
            "length_of_lists": 5,
            "primary_stadium": AVONDRONDE,
            "secondary_stadia": [HERCONTROLE, TWEEDE_HERCONTROLE, DERDE_HERCONTROLE]
        },
        {
            "number_of_lists": 2,
            "length_of_lists": 8,
            "primary_stadium": ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [TWEEDE_CONTROLE, DERDE_CONTROLE]
        },
        {
            "number_of_lists": 2,
            "length_of_lists": 8,
            "primary_stadium": ONDERZOEK_BUITENDIENST,
            "secondary_stadia": [TWEEDE_CONTROLE, DERDE_CONTROLE]
        },
        {
            "number_of_lists": 2,
            "length_of_lists": 4,
            "primary_stadium": WEEKEND_BUITENDIENST_ONDERZOEK,
            "secondary_stadia": [HERCONTROLE, TWEEDE_HERCONTROLE, DERDE_HERCONTROLE]
        }
    ]
}
