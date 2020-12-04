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

API_EXCEPTION_SEVERITY_ERROR = "ERROR"
API_EXCEPTION_SEVERITY_WARNING = "WARNING"
API_EXCEPTION_SEVERITY_INFO = "INFO"

ITINERARY_NOT_ENOUGH_CASES = {
    "severity": API_EXCEPTION_SEVERITY_INFO,
    "message": "Er zijn vandaag niet genoeg zaken die voldoen aan de ingestelde criteria. Neem contact op met je dagcoördinator of handhaver.",
    "title": "Helaas, geen looplijst mogelijk",
}
