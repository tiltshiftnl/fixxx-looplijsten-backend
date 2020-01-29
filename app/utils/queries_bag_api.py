import requests
from django.conf import settings
from utils.queries import get_import_adres
from time import sleep


def get_bag_search_query(address):
    sttnaam = address.get('postcode')
    hsnr = address.get('hsnr')

    hsltr = address.get('hsltr', '') or ''
    toev = address.get('toev', '') or ''

    query = '{} {} {}{}'.format(sttnaam, hsnr, hsltr, toev)

    return query.strip()

def do_bag_search_address(address):
    '''
    Search BAG using a BWV address
    '''
    query = get_bag_search_query(address)

    address_search = requests.get(settings.BAG_API_SEARCH_URL, params={'q': query})

    return address_search.json()

def do_bag_search_id(address):
    '''
    Search BAG using a BWV 'landelijk BAG ID'
    '''

    id = address['landelijk_bag']

    address_search = requests.get(settings.BAG_API_SEARCH_URL, params={'q': id})

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

def get_bag_data(wng_id):
    address = get_import_adres(wng_id)
    try:
        address_search = do_bag_search(address)
        sleep(0.125)

        # Do a request using the the objects href
        address_uri = address_search['results'][0]['_links']['self']['href']
        address_bag_data = requests.get(address_uri)

        return address_bag_data.json()

    except Exception as e:
        print('Requesting BAG data failed:')
        print(e)
        return {'error': str(e)}
