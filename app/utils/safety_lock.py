from django.http import Http404
from constance import config

def safety_lock(func):
    def wrapper(*args, **kwargs):
        if(config.ALLOW_DATA_ACCESS):
            return func(*args, **kwargs)
        else:
            raise Http404('Not allowed to access data')
    return wrapper
