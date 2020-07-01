# TODO: Tests for this
import logging
import requests
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


def get_cases():
    url = f'{settings.ZAKEN_API_URL}/cases'

    try:
        response = requests.get(url, timeout=1.5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'Could not get cases: {e}')

def datetime_to_date(date_time=None):
    if not date_time:
        return
    # return str(date_time.date())        
    # TODO: Temporary fix for debugging
    return str(datetime.now().date())
    
    

def push_case(case):
    url = f'{settings.ZAKEN_API_URL}/push/'

    street_name = case.get('street_name')
    street_number = case.get('street_number')

    suffix_letter = case.get('suffix_letter', '') or ''
    suffix = case.get('suffix', '') or ''

    postal_code = case.get('postal_code')

    address = f'{street_name} {street_number}{suffix_letter}{suffix}, {postal_code}'

    start_date = case.get('start_date', None)
    start_date = datetime_to_date(start_date)

    end_date = case.get('end_date', None)
    end_date = datetime_to_date(end_date)

    for i in range(3):
        try:
            data = {
                'identificatie': case['case_id'],
                'omschrijving': case['case_reason'],
                'toelichting': address,
                'startdatum': start_date,
            }

            if end_date:
                data['einddatum'] = end_date

            response = requests.post(url, timeout=2, json=data)
            return response
        except Exception as e:
            logger.error(f'Could not push cases: {e}')


def push_checked_action(case_id, check):
    url = f'{settings.ZAKEN_API_URL}/push-check-action/'

    for i in range(3):
        try:
            data = {
                'identificatie': case_id,
                'check_actie': check
            }
            response = requests.post(url, timeout=2, json=data)
            return response
        except Exception as e:
            logger.error(f'Could not push action: {e}')
