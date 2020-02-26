from datetime import datetime
from utils import queries
# TODO: Tests for this
'''
Helper function to parse and process BWV 'mededelingen' (statements) text
'''

def parse_date(raw_date):
    '''
    The BWV date for statements contains string dates in the following format: '17-OKT-19'
    This function parses this date and returns a universal date object
    '''

    months = ['JAN', 'FEB', 'MRT', 'APR', 'MEI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEC']
    raw_day, raw_month, raw_year = raw_date.split('-')

    year = int(raw_year) + 2000
    day = int(raw_day)
    month = months.index(raw_month) + 1

    date = datetime(year, month, day, 0, 0)
    return date


def parse_statement(raw_statements):
    '''
    Parses a raw statements string and normalizes the date
    '''
    DELIMITER = '[SPLIT]'
    raw_statements = raw_statements.replace('(', DELIMITER)
    raw_statements = raw_statements.replace('): ', DELIMITER)
    split_statements = raw_statements.split('\n')
    split_statements = split_statements[:-1]

    statements = []

    for text_statement in split_statements:
        user_code, raw_date, text = text_statement.split(DELIMITER)
        user = queries.get_toezichthouder_name(user_code)
        date = parse_date(raw_date)

        statement = {
            'user': user,
            'date': date,
            'statement': text
        }

        statements.append(statement)

    return statements
