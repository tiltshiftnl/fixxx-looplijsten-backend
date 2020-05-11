from constance import config
from django.http import Http404


def safety_lock(func):
    '''
    A decorator function that allows or blocks data access according to the admin's configuration
    '''

    def wrapper(*args, **kwargs):
        if (config.ALLOW_DATA_ACCESS):
            return func(*args, **kwargs)
        else:
            raise Http404('Not allowed to access data')

    return wrapper
