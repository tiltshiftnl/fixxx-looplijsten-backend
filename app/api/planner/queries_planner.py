from utils.query_helpers import do_query

def to_query_list(list):
    query_string = str(list)[1:-1]
    return query_string

def get_cases(starting_date, projects, stages):
    projects_query_list = to_query_list(projects)
    stages_query_list = to_query_list(stages)

    query = """
            SELECT
              DISTINCT zaak_id,
              import_wvs.beh_oms AS case_reason,
              import_adres.postcode AS postal_code,
              import_adres.sttnaam AS street_name,
              import_adres.hsnr AS street_number,
              import_adres.hsltr AS suffix_letter,
              import_adres.toev AS suffix,
              import_stadia.sta_oms AS stadium,
              import_stadia.sta_nr AS sta_nr,
              import_adres.wzs_lon AS lng,
              import_adres.wzs_lat as lat
            FROM
              import_wvs
            INNER JOIN
              import_stadia ON import_wvs.adres_id = import_stadia.adres_id
            INNER JOIN
              import_adres ON import_wvs.adres_id = import_adres.adres_id
            AND import_wvs.begindatum > '{}'
            AND import_stadia.einddatum is Null
            AND import_stadia.peildatum < NOW()
            AND beh_oms IN ({})
            AND sta_oms IN ({})
            ORDER BY sta_nr desc
            """.format(starting_date, projects_query_list, stages_query_list)

    executed_query = do_query(query)
    return executed_query