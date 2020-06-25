import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def get_cases():
    url = f'{settings.ZAKEN_API_URL}/cases'

    try:
        response = requests.get(url, timeout=1.5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'Could not get cases: {e}')


def push_case(case_id):
    url = f'{settings.ZAKEN_API_URL}/push/'

    for i in range(3):
        try:
            data = {"case_id": case_id}
            response = requests.post(url, timeout=1.5, json=data)
            return response
        except Exception as e:
            logger.error(f'Could not push cases: {e}')
