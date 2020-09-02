# TODO: Tests for this
import logging
from datetime import datetime

import requests
from apps.visits.models import Visit
from django.conf import settings
from tenacity import after_log, retry, stop_after_attempt, wait_random
from utils.queries import get_case, get_import_stadia
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


def get_headers():
    token = settings.SECRET_KEY_TOP_ZAKEN
    headers = {
        "Authorization": f"{token}",
        "content-type": "application/json",
    }
    return headers


def date_to_string(date):
    if date:
        return str(date)

    return None


def stadium_bwv_to_push_state(stadium):
    """ Transforms a stadium to be compatible with zaken-backend """
    return {
        "name": stadium.get("sta_oms"),
        "start_date": date_to_string(stadium.get("begindatum")),
        "end_date": date_to_string(stadium.get("einddatum", None)),
        "gauge_date": date_to_string(stadium.get("peildatum", None)),
        "invoice_identification": stadium.get("invordering_identificatie"),
    }


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=0, max=0.03),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_case(case_id):
    logger.info(f"Pushing case {case_id}")

    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings. Exit push.")
        return {}
    elif not settings.PUSH_ZAKEN:
        logger.info("Pushes disabled. Exit push.")
        return {}

    case = get_case(case_id)
    url = f"{settings.ZAKEN_API_URL}/push/"

    start_date = date_to_string(case.get("start_date"))
    end_date = date_to_string(case.get("end_date", None))
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
        data["end_date"] = end_date

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    logger.info(f"Finished pushing case {case_id}")
    return response


@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def push_checked_action(case_id, check):
    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings")
        return {}
    elif not settings.PUSH_ZAKEN:
        logger.info("Pushes disabled")
        return {}

    url = f"{settings.ZAKEN_API_URL}/push-check-action/"
    data = {"identification": case_id, "check_action": check}
    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    return response


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=0, max=0.03),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_new_visit_to_zaken_action(visit_id, subject, parameters, notes):
    logger.info(f"Pushing visit {visit_id} to zaken")

    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings. Exit push.")
        return {}
    elif not settings.PUSH_ZAKEN:
        logger.info("Pushes disabled. Exit push.")
        return {}

    try:
        visit = Visit.objects.get(id=visit_id)
        case = visit.itinerary_item.case
    except Visit.DoesNotExist:
        return {}

    url = f"{settings.ZAKEN_API_URL}/push/"

    data = {
        "case_identification": case.identification,
        "subject": subject,
        "parameters": parameters,
        "notes": notes,
    }

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    logger.info(f"Finished pushing case {case.identification}")

    visit.thread_id = response.data["thread_id"]
    visit.save()
    return response


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=0, max=0.03),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_updated_visit_to_zaken_action(visit_id, subject, parameters, notes):
    logger.info(f"Pushing visit {visit_id} to zaken")

    if not settings.ZAKEN_API_URL:
        logger.info("ZAKEN_API_URL is not configured in settings. Exit push.")
        return {}
    elif not settings.PUSH_ZAKEN:
        logger.info("Pushes disabled. Exit push.")
        return {}

    try:
        visit = Visit.objects.get(id=visit_id)
        case = visit.itinerary_item.case
    except Visit.DoesNotExist:
        return {}

    url = f"{settings.ZAKEN_API_URL}/push/"

    data = {"parameters": parameters, "notes": notes, "thread_id": visit.thread_id}

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    logger.info(f"Finished pushing updated case {case.identification}")

    return response
