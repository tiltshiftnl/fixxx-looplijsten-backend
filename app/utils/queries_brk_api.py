import requests
from constance.backends.database.models import Constance

def brk_request(func):
    '''
    A decorator function that makes sure a valid token exists to do requests to BRK
    '''

    def wrapper(request, *args, **kwargs):
        '''
        This wrapper makes sure a valid BRK token exists before doing a request
        '''
        token = get_token()
        expiry = get_expiry()
        is_valid = is_valid_token(token, expiry)

        if not is_valid:
            request_new_token()

        return func(request, *args, **kwargs)

    def is_valid_token(token, expiry):
        return token and not is_expired(expiry)

    def is_expired(expiry):

        # TODO: Implement this once we have the necessary credentials
        return False

    def get_token():
        token, created = Constance.objects.get_or_create(key='BRK_AUTHENTICATION_TOKEN')
        return token

    def get_expiry():
        expiry, created = Constance.objects.get_or_create(key='BRK_AUTHENTICATION_TOKEN_EXPIRY')
        return expiry

    def request_new_token():
        # TODO: Implement this once we have the necessary credentials
        return

    return wrapper

def get_brk_data():
    '''
    Do a brk request. This is a temporary adress
    '''
    try:
        brk_data = requests.get('https://api.data.amsterdam.nl/brk/gemeente/')
        return brk_data.json()

    except Exception as e:
        print('Requesting BRK data failed:')
        print(e)
        return {'error': str(e)}
