# TODO: Tests for this
import logging
from datetime import datetime

import requests
from django.conf import settings
from tenacity import after_log, retry, stop_after_attempt, wait_random
from utils.queries import get_import_stadia
from utils.queries_bag_api import get_bag_id

logger = logging.getLogger(__name__)


def get_cases():
    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings")
        return {}

    url = f"{settings.ZAKEN_API_URL}/cases"

    try:
        response = requests.get(url, timeout=1.5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Could not get cases: {e}")


def datetime_to_date(date_time=None):
    if not date_time:
        return
    # return str(date_time.date())
    # TODO: Temporary fix for debugging
    return str(datetime.now().date())


def get_headers():
    token = settings.SECRET_KEY_TOP_ZAKEN
    headers = {
        "Authorization": f"{token}",
        "content-type": "application/json",
    }
    return headers


def stadium_bwv_to_push_state(stadium):
    """ Transforms a stadium to be compatible with zaken-backend """
    return {
        "name": stadium.get("sta_oms"),
        "start_date": datetime_to_date(stadium.get("begindatum")),
        "end_date": datetime_to_date(stadium.get("einddatum")),
        "gauge_date": datetime_to_date(stadium.get("peildatum")),
        "invoice_identification": stadium.get("invordering_identificatie"),
    }


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=1, max=2),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_case(case):
    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings")
        return {}

    url = f"{settings.ZAKEN_API_URL}/push/"

    start_date = case.get("start_date")
    start_date = datetime_to_date(start_date)

    end_date = case.get("end_date", None)
    case_id = case.get("case_id")

    stadia = get_import_stadia(case_id)
    states = [stadium_bwv_to_push_state(stadium) for stadium in stadia]

    data = {
        "identification": case_id,
        "case_type": case["case_reason"],
        "bag_id": get_bag_id(case),
        "start_date": start_date,
        "states": states,
    }

    if end_date:
        end_date = datetime_to_date(end_date)
        data["end_date"] = end_date

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    return response


@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def push_checked_action(case_id, check):
    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings")
        return {}

    url = f"{settings.ZAKEN_API_URL}/push-check-action/"
    data = {"identification": case_id, "check_action": check}
    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    return response
