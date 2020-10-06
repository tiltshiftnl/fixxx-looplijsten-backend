SITUATION_NOBODY_PRESENT = "nobody_present"
SITUATION_NO_COOPERATION = "no_cooperation"
SITUATION_ACCESS_GRANTED = "access_granted"

SITUATIONS = (
    (SITUATION_NOBODY_PRESENT, "Niemand aanwezig"),
    (SITUATION_NO_COOPERATION, "Geen medewerking"),
    (SITUATION_ACCESS_GRANTED, "Toegang verleend"),
)

OBSERVATION_MALFUNCTIONING_DOORBEL = "malfunctioning_doorbell"
OBSERVATION_INTERCOM = "intercom"
OBSERVATION_HOTEL_FURNISHED = "hotel_furnished"
OBSERVATION_VACANT = "vacant"
OBSERVATION_LIKELY_INHABITED = "likely_inhabited"

OBSERVATIONS = (
    (OBSERVATION_MALFUNCTIONING_DOORBEL, "Bel functioneert niet"),
    (OBSERVATION_INTERCOM, "Contact via intercom"),
    (OBSERVATION_HOTEL_FURNISHED, "Hotelmatig ingericht"),
    (OBSERVATION_VACANT, "Leegstaand"),
    (OBSERVATION_LIKELY_INHABITED, "Vermoedelijk bewoond"),
)

SUGGEST_VISIT_WEEKEND = "weekend"
SUGGEST_VISIT_DAYTIME = "daytime"
SUGGEST_VISIT_EVENING = "evening"
SUGGEST_VISIT_UNKNOWN = "unknown"

SUGGEST_NEXT_VISIT = (
    (SUGGEST_VISIT_WEEKEND, "Weekend"),
    (SUGGEST_VISIT_DAYTIME, "Overdag"),
    (SUGGEST_VISIT_EVENING, "'s Avonds"),
    (SUGGEST_VISIT_UNKNOWN, "Onbekend"),
)