from utils.query_helpers import do_query

def to_query_list(list):
    query_string = str(list)[1:-1]
    return query_string


def get_eligible_stadia(stages):
    query = """
            SELECT
            sta_oms AS stadium,
            sta_nr AS sta_nr,
            stadia_id,
            einddatum
            FROM import_stadia
            WHERE einddatum is Null
            AND peildatum < NOW()
            AND sta_oms IN ({})
            """.format(stages)

    stadia = do_query(query)

    stadia_dictionary = {}
    for stadium in stadia:
        stadia_id = stadium['stadia_id']
        case_id_raw = stadia_id.split('_')
        case_id_raw.pop()
        case_id = '_'.join(case_id_raw)
        stadia_dictionary[case_id] = stadium

    return stadia_dictionary

def get_eligible_cases(starting_date, projects_query_list):
    query = """
            SELECT
              DISTINCT zaak_id AS case_id,
              import_wvs.beh_oms AS case_reason,
              import_adres.postcode AS postal_code,
              import_adres.sttnaam AS street_name,
              import_adres.hsnr AS street_number,
              import_adres.hsltr AS suffix_letter,
              import_adres.toev AS suffix,
              import_adres.wzs_lon AS lng,
              import_adres.wzs_lat as lat
            FROM import_wvs
            INNER JOIN
              import_adres ON import_adres.adres_id = import_wvs.adres_id
            WHERE begindatum > '{}'
            AND beh_oms IN ({})
            """.format(starting_date, projects_query_list)

    cases = do_query(query)
    return cases

def get_cases(starting_date, projects, stages):
    projects_query_list = to_query_list(projects)
    stages_query_list = to_query_list(stages)

    eligible_cases = get_eligible_cases(starting_date, projects_query_list)
    eligible_stages = get_eligible_stadia(stages_query_list)

    filtered_cases = []

    for case in eligible_cases:
        case_id = case.get('case_id')
        stage = eligible_stages.get(case_id, None)

        if stage:
            filtered_cases.append({**case, **stage})

    return filtered_cases
