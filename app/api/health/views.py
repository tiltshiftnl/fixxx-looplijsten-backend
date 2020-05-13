import logging

from django.conf import settings

from api.health.utils import assert_health_database_tables, assert_health_generic, get_health_response
from api.health.utils import get_bwv_sync_times

SUCCESS_DICTIONARY_DEFAULT = {'message': 'Connectivity OK'}
SUCCESS_DICTIONARY_BWV = {'message': 'BWV Connectivity OK'}
BWV_TABLES = [
    'bwv_benb_meldingen',
    'bwv_hotline_bevinding',
    'bwv_medewerkers',
    'bwv_personen',
    'bwv_personen_hist',
    'bwv_vakantieverhuur',
    'bwv_vakantieverhuur_annuleren',
    'bwv_woningen',
    'import_adres',
    'import_stadia',
    'import_wvs',
]

LOGGER = logging.getLogger(__name__)


def health_default(request):
    def assert_default_health():
        assert_health_generic(database_name=settings.DEFAULT_DATABASE_NAME)

    return get_health_response(assert_default_health, SUCCESS_DICTIONARY_DEFAULT)


def health_bwv(request):
    def assert_bwv_health():
        LOGGER.info('BWV Health check generic')
        assert_health_generic(database_name=settings.BWV_DATABASE_NAME)
        LOGGER.info('BWV Health check generic Done')
        LOGGER.info('BWV Health check tables')
        assert_health_database_tables(database_name=settings.BWV_DATABASE_NAME, tables=BWV_TABLES)
        LOGGER.info('BWV Health check tables Done')

    LOGGER.info('BWV Health check getting sync times')
    sync_times = get_bwv_sync_times()
    LOGGER.info('BWV Health check getting sync times Done')
    LOGGER.info('BWV Health formatting sync times')
    sync_times = [{'start': str(sync_time['start']), 'finished': str(sync_time['finished'])}
                  for sync_time in sync_times]
    LOGGER.info('BWV Health formatting sync times Done')
    LOGGER.info('BWV Health setting success dictionary')
    success_dict = SUCCESS_DICTIONARY_BWV.copy()
    success_dict['sync_times'] = sync_times
    LOGGER.info('BWV Health setting success dictionary Done')

    return get_health_response(assert_bwv_health, success_dict)
