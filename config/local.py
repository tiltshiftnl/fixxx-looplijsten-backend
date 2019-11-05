import os
from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ALLOWED_HOSTS = ['0.0.0.0', 'localhost']
    CORS_ORIGIN_WHITELIST = (
        'http://localhost:3000',
    )
    CORS_ORIGIN_ALLOW_ALL = False
