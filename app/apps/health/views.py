from apps.health.utils import (
    assert_bwv_health,
    assert_health_database_tables,
    assert_health_generic,
    get_bwv_sync_times,
    get_health_response,
)
from django.conf import settings

SUCCESS_DICTIONARY_DEFAULT = {"message": "Connectivity OK"}
SUCCESS_DICTIONARY_BWV = {"message": "BWV Connectivity OK"}


def health_default(request):
    def assert_default_health():
        assert_health_generic(database_name=settings.DEFAULT_DATABASE_NAME)

    return get_health_response(assert_default_health, SUCCESS_DICTIONARY_DEFAULT)


def health_bwv(request):
    sync_times = get_bwv_sync_times()
    sync_times = [
        {"start": str(sync_time["start"]), "finished": str(sync_time["finished"])}
        for sync_time in sync_times
    ]
    success_dict = SUCCESS_DICTIONARY_BWV.copy()
    success_dict["sync_times"] = sync_times

    return get_health_response(assert_bwv_health, success_dict)
