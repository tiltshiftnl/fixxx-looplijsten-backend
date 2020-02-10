STARTING_DATE = "2019-01-01 00:00:00"

PROJECTS = [
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
    # TODO: Add sahara stuff
]

STAGES = [
    "2de Controle",
    "2de hercontrole",
    "3de Controle",
    "3de hercontrole",
    "Avondronde",
    "Hercontrole",
    "Onderzoek advertentie",
    "Onderzoek buitendienst",
    "Weekend buitendienstonderzoek"
    # TODO: add issue melding here
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
    "days": [
        {
            "day": "monday",
            "lists": [
                {
                    "name": "Ochtend",
                    "number_of_lists": 4,
                    "length_of_lists": 6
                }

            ]
        },
        {
            "day": "tuesday",
            "lists": [
                {
                    "name": "Ochtend",
                    "number_of_lists": 4,
                    "length_of_lists": 8
                },
                {
                    "name": "Middag",
                    "number_of_lists": 4,
                    "length_of_lists": 8
                },
                {
                    "name": "Avond",
                    "number_of_lists": 4,
                    "length_of_lists": 5
                }
            ]
        }
    ]
}
