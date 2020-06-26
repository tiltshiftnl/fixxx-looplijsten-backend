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


def push_case(case):
    url = f'{settings.ZAKEN_API_URL}/push/'

    street_name = case.get('street_name')
    street_number = case.get('street_number')

    suffix_letter = case.get('suffix_letter', '') or ''
    suffix = case.get('suffix', '') or ''

    postal_code = case.get('postal_code')

    address = f'{street_name} {street_number}{suffix_letter}{suffix}, {postal_code}'

    for i in range(3):
        try:
            data = {
                'identificatie': case['case_id'],
                'omschrijving': case['case_reason'],
                'toelichting': address
            }
            response = requests.post(url, timeout=2, json=data)
            return response
        except Exception as e:
            logger.error(f'Could not push cases: {e}')
