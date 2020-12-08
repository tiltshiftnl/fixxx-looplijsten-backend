# TODO: Tests for this
import logging
from datetime import datetime

import requests
from django.conf import settings
from tenacity import after_log, retry, stop_after_attempt, wait_random
from utils.queries import get_case, get_import_stadia
from utils.queries_bag_api import get_bag_id

logger = logging.getLogger(__name__)


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


def assert_allow_push():
    assert settings.ZAKEN_API_URL, "ZAKEN_API_URL is not configured in settings."
    assert settings.PUSH_ZAKEN, "Pushes disabled"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=0, max=0.3),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_new_visit_to_zaken_action(visit, authors):
    logger.info(f"Pushing visit {visit.id} to zaken")

    assert_allow_push()

    url = f"{settings.ZAKEN_API_URL}/visits/create_visit_from_top/"

    data = {
        "case_identification": visit.case_id.case_id,
        "start_time": str(visit.start_time),
        "observations": visit.observations,
        "situation": visit.situation,
        "authors": authors,
        "can_next_visit_go_ahead": visit.can_next_visit_go_ahead,
        "can_next_visit_go_ahead_description": visit.can_next_visit_go_ahead_description,
        "suggest_next_visit": visit.suggest_next_visit,
        "suggest_next_visit_description": visit.suggest_next_visit_description,
        "notes": visit.description,
    }

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    response.raise_for_status()

    logger.info(f"Finished pushing case {visit.case_id.case_id}")
    return response


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=0, max=0.3),
    reraise=False,
    after=after_log(logger, logging.ERROR),
)
def push_updated_visit_to_zaken_action(visit, authors):
    logger.info(f"Pushing visit {visit.id} to zaken")

    assert_allow_push()

    url = f"{settings.ZAKEN_API_URL}/visits/update_visit_from_top/"

    data = {
        "case_identification": visit.case_id.case_id,
        "start_time": str(visit.start_time),
        "observations": visit.observations,
        "situation": visit.situation,
        "authors": authors,
        "can_next_visit_go_ahead": visit.can_next_visit_go_ahead,
        "can_next_visit_go_ahead_description": visit.can_next_visit_go_ahead_description,
        "suggest_next_visit": visit.suggest_next_visit,
        "suggest_next_visit_description": visit.suggest_next_visit_description,
        "notes": visit.description,
    }

    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    response.raise_for_status()

    logger.info(f"Finished pushing updated case {visit.case_id.case_id}")

    return response
