from django.db import Error, connections
from django.http import HttpResponse
from django.conf import settings


def health_generic(request, database_name, success_message, error_message):
    try:
        with connections[database_name].cursor() as cursor:
            cursor.execute('select 1')
            assert cursor.fetchone()
    except Error:
        return HttpResponse(error_message, content_type='text/plain', status=500)
    else:
        return HttpResponse(success_message, content_type='text/plain', status=200)


def health_default(request):
    return health_generic(request,
                          settings.DEFAULT_DATABASE_NAME,
                          'Connectivity OK',
                          'Database connectivity failed',
                          )

def health_bwv(request):
    return health_generic(request,
                          settings.BWV_DATABASE_NAME,
                          'BWV Connectivity OK',
                          'BWV Database connectivity failed',
                          )
