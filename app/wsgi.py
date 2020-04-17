import os
import logging
import signal
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

application = get_wsgi_application()

def service_shutdown(signum, frame):
    LOGGER = logging.getLogger(__name__)
    LOGGER.info('Service shutdown information Signum {}'.format(str(signum)))
    LOGGER.info('Service shutdown information Frame {}'.format(str(frame)))


# For debugging purposes, catch sigterm and sigint signals
signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)
