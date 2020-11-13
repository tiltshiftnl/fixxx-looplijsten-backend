ISSUEMELDING = "Issuemelding"
TERUGKOPPELING_SIA = "Terugkoppeling SIA"
VERVOLG_SIA = "Vervolg SIA"

STARTING_FROM_DATE = "2019-01-01"

EXCLUDE_STADIA = (
    TERUGKOPPELING_SIA,
    VERVOLG_SIA,
)

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
