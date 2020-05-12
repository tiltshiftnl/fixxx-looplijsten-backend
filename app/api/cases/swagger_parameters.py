from drf_yasg import openapi

"""
Manual parameters for the unplanned view in Swagger API documentation
"""
date = openapi.Parameter(
    name='date',
    in_=openapi.IN_QUERY,
    description="Date",
    type=openapi.FORMAT_DATE)

stadium = openapi.Parameter(
    name='stadium',
    in_=openapi.IN_QUERY,
    description="Stadium",
    type=openapi.TYPE_STRING)

unplanned_parameters = [date, stadium]

"""
Manual parameters for the case search view in Swagger API documentation
"""
postal_code = openapi.Parameter(
    name='postalCode',
    in_=openapi.IN_QUERY,
    required=True,
    description="Postal Code",
    type=openapi.TYPE_STRING)

street_number = openapi.Parameter(
    name='streetNumber',
    in_=openapi.IN_QUERY,
    required=True,
    description="Street Number",
    type=openapi.TYPE_STRING)

suffix = openapi.Parameter(
    name='suffix',
    in_=openapi.IN_QUERY,
    required=False,
    description="Suffix",
    default='',
    type=openapi.TYPE_STRING)

case_search_parameters = [postal_code, street_number, suffix]
