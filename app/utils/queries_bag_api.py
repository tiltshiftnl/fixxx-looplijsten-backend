import requests
import logging
from django.conf import settings
from utils.queries import get_import_adres
from circuitbreaker import circuit

logger = logging.getLogger(__name__)

def get_bag_search_query(address):
    '''
    Constructs a BAG search query using the address data
    '''
    sttnaam = address.get('postcode')
    hsnr = address.get('hsnr')

    hsltr = address.get('hsltr', '') or ''
    toev = address.get('toev', '') or ''

    query = '{} {} {}{}'.format(sttnaam, hsnr, hsltr, toev)

    return query.strip()

@circuit
def do_bag_search_address(address):
    '''
    Search BAG using a BWV address
    '''
    query = get_bag_search_query(address)

    address_search = requests.get(
        settings.BAG_API_SEARCH_URL,
        params={'q': query},
        timeout=1.5
    )

    return address_search.json()

@circuit
def do_bag_search_id(address):
    '''
    Search BAG using a BWV 'landelijk BAG ID'
    '''

    id = address['landelijk_bag']

    address_search = requests.get(
        settings.BAG_API_SEARCH_URL,
        params={'q': id},
        timeout=1.5
    )

    return address_search.json()

def do_bag_search(address):
    '''
    Search BAG. Uses a BAG id, or an address from BWV. Both contain inconsistencies in BWV.
    Here they are used together to get the best results.
    '''

    # First search using an addresss
    address_search = do_bag_search_address(address)

    # If that search didn't give any results, try using the Landelijk BAG id
    if(address_search['count'] == 0):
        address_search = do_bag_search_id(address)

    return address_search

@circuit
def get_bag_data(wng_id):
    address = get_import_adres(wng_id)
    try:
        address_search = do_bag_search(address)

        # Do a request using the the objects href
        address_uri = address_search['results'][0]['_links']['self']['href']
        address_bag_data = requests.get(
            address_uri,
            timeout=1.5
        )

        return address_bag_data.json()

    except Exception as e:
        logger.error('Requesting BAG data failed: {}'.format(str(e)))

        error_objects = {
            'error': str(e),
            'wng_id': wng_id,
            'api_url': settings.BAG_API_SEARCH_URL,
            'address': address,
        }
        return error_objects
