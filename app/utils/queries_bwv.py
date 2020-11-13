from utils.query_helpers import do_query


def get_bwv_tables():
    """
    Gets bwv tables and columns
    """

    query = """
            SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
            """

    args = {}
    return do_query(query, args)


def get_bwv_columns(table_name):
    """
    Gets bwv columns by table_name
    """

    query = """
            SELECT column_name FROM information_schema.columns WHERE table_name = %(table_name)s;
            """

    args = {"table_name": table_name}
    return do_query(query, args)
