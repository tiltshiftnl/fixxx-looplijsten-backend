from django.db import Error, connections
from django.http import HttpResponse
from django.conf import settings

SUCCESS_MESSAGE_DEFAULT = 'Connectivity OK'
ERROR_MESSAGE_DEFAULT = 'Database connectivity failed'
SUCCESS_MESSAGE_BWV = 'BWV Connectivity OK'
ERROR_MESSAGE_BWV = 'BWV Database connectivity failed'

def health_generic(request, database_name, success_message, error_message):
    try:
        cursor = connections[database_name].cursor()
        cursor.execute('select 1')
        assert cursor.fetchone()
    except Error:
        return HttpResponse(error_message, content_type='text/plain', status=500)
    else:
        return HttpResponse(success_message, content_type='text/plain', status=200)


def health_default(request):
    return health_generic(request=request,
                          database_name=settings.DEFAULT_DATABASE_NAME,
                          success_message=SUCCESS_MESSAGE_DEFAULT,
                          error_message=ERROR_MESSAGE_DEFAULT
                          )

def health_bwv(request):
    return health_generic(request=request,
                          database_name=settings.BWV_DATABASE_NAME,
                          success_message=SUCCESS_MESSAGE_BWV,
                          error_message=ERROR_MESSAGE_BWV
                          )
