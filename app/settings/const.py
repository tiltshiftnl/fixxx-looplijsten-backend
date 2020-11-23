WEEK_DAYS = [
    "zondag",
    "maandag",
    "dinsdag",
    "woensdag",
    "donderdag",
    "vrijdag",
    "zaterdag",
]
WEEK_DAYS_CHOICES = [[i, wd] for i, wd in enumerate(WEEK_DAYS)]

ISSUEMELDING = "Issuemelding"
TERUGKOPPELING_SIA = "Terugkoppeling SIA"
VERVOLG_SIA = "Vervolg SIA"

STARTING_FROM_DATE = "2019-01-01"

EXCLUDE_STADIA = (
    TERUGKOPPELING_SIA,
    VERVOLG_SIA,
)

POSTAL_CODE_RANGES = [
    {"range_start": 1000, "range_end": 1109},
]

EXAMPLE_PLANNER_SETTINGS = {
    "opening_date": "2019-01-01",
    "projects": [],
    # Optional postal code settings
    "postal_codes": [{"range_start": 1000, "range_end": 1109}],
    "postal_code_ranges": [{"range_start": 1000, "range_end": 1109}],
    "days": {
        "monday": {
            "day": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
            "evening": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
        },
        "tuesday": {
            "day": {},
            "evening": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
        },
        "wednesday": {
            "day": {},
            "evening": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
        },
        "thursday": {
            "day": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
            "evening": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
        },
        "friday": {
            "day": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
            "evening": {
                "length_of_list": 6,
                "secondary_stadia": [],
            },
        },
        "saturday": {
            "day": {
                "length_of_list": 6,
                "secondary_stadia": [],
            }
        },
        "sunday": {
            "day": {
                "length_of_list": 6,
                "secondary_stadia": [],
            }
        },
    },
}

API_EXCEPTION_SEVERITY_ERROR = "ERROR"
API_EXCEPTION_SEVERITY_WARNING = "WARNING"
API_EXCEPTION_SEVERITY_INFO = "INFO"

ITINERARY_NOT_ENOUGH_CASES = {
    "severity": API_EXCEPTION_SEVERITY_INFO,
    "message": "Er zijn vandaag niet genoeg zaken die voldoen aan de ingestelde criteria. Neem contact op met je dagcoördinator of handhaver.",
    "title": "Helaas, geen looplijst mogelijk",
}

EXAMPLE_DAY_SETTINGS = {
    "opening_date": "2019-01-01",
    "projects": [],
    "postal_codes": [{"range_start": 1000, "range_end": 1109}],
    "postal_code_ranges": [{"range_start": 1000, "range_end": 1109}],
    "length_of_list": 6,
    "secondary_stadia": [],
}
