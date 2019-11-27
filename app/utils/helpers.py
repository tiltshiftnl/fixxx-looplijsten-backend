import re
from datetime import datetime

def get_postal_code(text):
    items = re.split('(\d{4})\s*([A-Z]{2})', text)
    postal_code_dict = {
        'address': items[0].strip(),
        'postal_code_area': items[1],
        'postal_code_street': items[2],
        'stadium': items[3]
    }
    return postal_code_dict


def get_days_in_range(start_date, end_date):
    '''
    Return the number of days within a range
    Any days that fall outside of the current year are not counted
    '''
    current_year = datetime.now().year
    start_year = start_date.year
    end_year = end_date.year

    # Normal case, when both dates fall into the current year
    if start_year == current_year and end_year == current_year:
        return (end_date - start_date).days
    if start_year != current_year and end_year == current_year:
        # If the start date doesn't fall in the current year, start counting from the first day
        start_date = datetime(current_year, 1, 1)
        return (end_date - start_date).days

    return 0
