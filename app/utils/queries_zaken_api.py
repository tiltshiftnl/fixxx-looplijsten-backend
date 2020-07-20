# TODO: Tests for this
import logging
import requests
from django.conf import settings
from datetime import datetime
from tenacity import retry, stop_after_attempt, after_log
from utils.queries_bag_api import get_bag_id

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
    
def get_headers():
    token = settings.SECRET_KEY_TOP_ZAKEN
    headers = {
        'Authorization': f"{token}",
        'content-type': "application/json",
    }  
    return headers

def push_case(case):    
    url = f'{settings.ZAKEN_API_URL}/push/'

    start_date = case.get('start_date')
    start_date = datetime_to_date(start_date)

    end_date = case.get('end_date', None)    

    data = {
        'identification': case['case_id'],
        'case_type': case['case_reason'],
        'bag_id': get_bag_id(case),
        'start_date': start_date,
    }

    if end_date:
        end_date = datetime_to_date(end_date)
        data['end_date'] = end_date

    @retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
    def push_case_request(data):
        response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
        return response

    return push_case_request(data)

@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def push_checked_action(case_id, check):
    url = f'{settings.ZAKEN_API_URL}/push-check-action/'
    data = {'identification': case_id, 'check_action': check}    
    response = requests.post(url, timeout=0.5, json=data, headers=get_headers())
    return response

