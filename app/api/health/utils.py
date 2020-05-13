import logging
from django.db import connections
from django.http import JsonResponse

from utils.query_helpers import do_query

LOGGER = logging.getLogger(__name__)

def get_health_response(health_checks, success_dictionary):
    """
    Executes the given health_checks function, 
    and returns a response based on the function's success
    """
    try:
        health_checks()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse(success_dictionary, status=200)


def is_table_filled_query(table):
    """
    A fast query to check if a table is filled (with at least one entry)
    """
    return "SELECT reltuples::bigint FROM pg_catalog.pg_class WHERE relname = '{}'".format(table)


def assert_health_table(database_name, table):
    """
    Given a database and one table, checks if the table is filled with at least on entry
    """
    cursor = connections[database_name].cursor()
    query = is_table_filled_query(table)
    cursor.execute(query)
    row = cursor.fetchone()
    assert row[0] > 0, 'The {} table in {} is empty'.format(table, database_name)


def assert_health_database_tables(database_name, tables):
    """
    Given a database and it's tables, this checks if all tables are filled
    """
    LOGGER.info('Health Check TABLES')
    for table in tables:
        LOGGER.info('Health Check TABLE {}'.format(table))
        assert_health_table(database_name, table)
        LOGGER.info('Health Check TABLE {} DONE'.format(table))
    LOGGER.info('Health Check TABLES DONE')

def assert_health_generic(database_name):
    """
    A basic check to see if a connection with the given database can be made
    """
    LOGGER.info('Health Check GENERIC START')
    cursor = connections[database_name].cursor()
    LOGGER.info('Health Check GENERIC CURSOR DONE')
    cursor.execute('select 1')
    LOGGER.info('Health Check EXECUTE DONE')
    assert cursor.fetchone()


def get_bwv_sync_times():
    query = """SELECT start, finished FROM sync_log ORDER BY start DESC"""

    executed_query = do_query(query)

    return executed_query
