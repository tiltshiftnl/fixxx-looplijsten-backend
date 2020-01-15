import requests
from datetime import datetime, timedelta
from constance.backends.database.models import Constance
from django.conf import settings

def brk_request(func):
    '''
    A decorator function that makes sure a valid token exists to do requests to BRK
    '''

    def wrapper(request, *args, **kwargs):
        '''
        This wrapper makes sure a valid BRK token exists before doing a request
        '''
        expiry = get_expiry()

        if expiry == '' or expiry < datetime.now():
            request_new_token()

        return func(request, *args, **kwargs)

    return wrapper

def get_token():
    key = settings.CONSTANCE_BRK_AUTHENTICATION_TOKEN_KEY
    token, created = Constance.objects.get_or_create(key=key)
    return token.value

def get_expiry():
    key = settings.CONSTANCE_BRK_AUTHENTICATION_TOKEN_EXPIRY_KEY
    expiry, created = Constance.objects.get_or_create(key=key)
    return expiry.value

def set_constance(key, value):
    constance_object, created = Constance.objects.get_or_create(key=key)
    constance_object.value = value
    constance_object.save()

def set_token(token):
    set_constance(
        settings.CONSTANCE_BRK_AUTHENTICATION_TOKEN_KEY,
        token
    )

def set_expiry(expiry):
    set_constance(
        settings.CONSTANCE_BRK_AUTHENTICATION_TOKEN_EXPIRY_KEY,
        expiry
    )

def request_new_token():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': settings.BRK_ACCESS_CLIENT_ID,
        'client_secret': settings.BRK_ACCESS_CLIENT_SECRET,
    }

    try:
        token_request_url = settings.BRK_ACCESS_URL

        response = requests.post(token_request_url, data=payload)
        response_json = response.json()

        access_token = response_json.get('access_token')
        set_token(access_token)

        expires_in = response_json.get('expires_in')
        expiry = datetime.now() + timedelta(seconds=expires_in)
        set_expiry(expiry)

    except Exception as e:
        print('Requesting BRK access token failed:')
        print(e)
        return {'error': str(e)}
    return

def get_brk_data(bag_id):
    '''
    Do a brk request. This is a temporary adress
    '''
    try:
        token = get_token()
        headers = {
            'Authorization': "Bearer {}".format(token),
            'content-type': "application/json",
        }

        request_uri = 'https://api.data.amsterdam.nl/brk/object-expand/?verblijfsobjecten__id={}'.format(
            bag_id)
        brk_data = requests.get(request_uri, headers=headers)

        return brk_data.json()

    except Exception as e:
        print('Requesting BRK data failed:')
        print(e)
        return {'error': str(e)}
