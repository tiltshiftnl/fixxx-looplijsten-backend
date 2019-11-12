from django.db import Error, connection
from django.http import HttpResponse


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('select 1')
            assert cursor.fetchone()
    except Error:
        error_msg = 'Database connectivity failed'
        return HttpResponse(error_msg, content_type='text/plain', status=500)
    else:
        return HttpResponse('Connectivity OK', content_type='text/plain', status=200)
