from __future__ import absolute_import
import logging
import time
from test_celery.celery import app
from api.cases.models import Case

LOGGER = logging.getLogger(__name__)

@app.task(bind=True, default_retry_delay=10)
def longtime_print(self, i):
    LOGGER.info('Celery longtime task begins')
    cases = Case.objects.all()
    for case in cases:
        time.sleep(5)
        LOGGER.info('Case: {}'.format(str(case)))
    LOGGER.info('long time task finished {}'.format(i))
    return 200
