import logging

import requests
from apps.itinerary.models import ItineraryItem
from celery import shared_task
from django.conf import settings
from utils.queries import get_case, get_import_stadia
from utils.queries_bag_api import get_bag_id
from utils.queries_zaken_api import (
    assert_allow_push,
    date_to_string,
    get_headers,
    stadium_bwv_to_push_state,
)

logger = logging.getLogger(__name__)

DEFAULT_RETRY_DELAY = 30 * 60
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 60


@shared_task(bind=True, default_retry_delay=DEFAULT_RETRY_DELAY)
def push_itinerary_item(self, pk):
    """
    Pushing the itinerary and case date is needed
    """
    logger.info(f"Pushing case for itinerary item {pk}")
    assert_allow_push()

    itinerary_item = ItineraryItem.objects.get(pk=pk)

    case_id = itinerary_item.case.case_id
    case = get_case(case_id)

    start_date = date_to_string(case.get("start_date"))
    end_date = date_to_string(case.get("end_date", None))

    stadia = get_import_stadia(case_id)
    states = [stadium_bwv_to_push_state(stadium) for stadium in stadia]

    team_members = itinerary_item.itinerary.team_members.all()
    users = [team_member.user.email for team_member in team_members]

    data = {
        "identification": case_id,
        "case_type": case["case_reason"],
        "bag_id": get_bag_id(case),
        "start_date": start_date,
        "states": states,
        "users": users,
    }

    if end_date:
        data["end_date"] = end_date

    url = f"{settings.ZAKEN_API_URL}/push/"

    try:
        response = requests.post(
            url,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            json=data,
            headers=get_headers(),
        )
        response.raise_for_status()

        response_json = response.json()

        itinerary_item.external_state_id = response_json["state"]["id"]
        itinerary_item.save()

        logger.info(f"Finished pushing case {case_id}")

        return response
    except Exception as exception:
        self.retry(exc=exception)