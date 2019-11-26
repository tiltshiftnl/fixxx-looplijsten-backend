from django.conf import settings
from django.db import Error, connections

def query_to_list(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]

def do_query(query):
    try:
        with connections[settings.BWV_DATABASE_NAME].cursor() as cursor:
            cursor.execute(query)
            return query_to_list(cursor)
    except Error:
        return {}

def get_search_results(postal_code, street_number, suffix):
    suffix_query = ''
    if suffix:
        suffix_query = """AND toev = '{}'""".format(suffix)

    query = """
              WITH results AS (
                SELECT
                  import_adres.postcode AS postal_code,
                  import_adres.sttnaam AS street_name,
                  import_adres.hsnr AS street_number,
                  import_adres.toev AS suffix,
                  import_stadia.sta_oms AS stadium,
                  import_stadia.stadia_id AS stadium_id,
                  import_wvs.zaak_id AS case_id,
                  import_stadia.date_created
                FROM import_adres INNER JOIN import_stadia ON import_adres.adres_id = import_stadia.adres_id
                INNER JOIN import_wvs ON import_stadia.adres_id = import_wvs.adres_id
                AND postcode = '{}'
                AND hsnr = '{}'
                {}
                ORDER BY case_id ASC, import_stadia.date_created DESC
              )
              SELECT DISTINCT ON (case_id) * FROM RESULTS
              """.format(postal_code, street_number, suffix_query)

    return do_query(query)

def get_related_case_ids(case_id):
    query = """
            SELECT DISTINCT ON (import_wvs.zaak_id)
              import_adres.adres_id,
              import_adres.wng_id
            FROM import_adres INNER JOIN import_stadia ON import_adres.adres_id = import_stadia.adres_id
            INNER JOIN import_wvs ON import_stadia.adres_id = import_wvs.adres_id
            AND zaak_id = '{}'
              """.format(case_id)
    return do_query(query)


def get_bwv_hotline_bevinding(wng_id):
    query = """
            SELECT
              toez_hdr1_code,
              bevinding_datum,
              bevinding_tijd,
              hit,
              opmerking,
              volgnr_bevinding
            FROM bwv_hotline_bevinding WHERE wng_id = '{}'
            ORDER BY volgnr_bevinding ASC
            """.format(wng_id)

    return do_query(query)

def get_bwv_hotline_melding(wng_id):
    query = """
            SELECT
              melding_datum,
              melder_anoniem,
              melder_naam,
              melder_emailadres,
              melder_telnr,
              situatie_schets
            FROM bwv_hotline_melding WHERE wng_id = '{}'
            ORDER BY melding_datum ASC
            """.format(wng_id)

    return do_query(query)

def get_bwv_personen(adres_id):
    query = """
            SELECT
              naam,
              voorletters,
              geslacht,
              geboortedatum,
              vestigingsdatum_adres
            FROM bwv_personen WHERE ads_id_wa = '{}'
            ORDER BY vestigingsdatum_adres DESC, geboortedatum ASC
            """.format(adres_id)

    return do_query(query)

def get_import_adres(wng_id):
    query = """
            SELECT
              sttnaam,
              hsnr,
              toev,
              postcode,
              sbw_omschr,
              kmrs,
              a_dam_bag
            FROM import_adres WHERE wng_id = '{}'
            """.format(wng_id)

    return do_query(query)[0]

def get_import_stadia(adres_id):
    query = """
            SELECT
            sta_oms,
            begindatum,
            einddatum,
            peildatum,
            sta_nr
          FROM import_stadia WHERE adres_id = '{}'
          ORDER BY sta_nr DESC
          """.format(adres_id)

    return do_query(query)

def get_import_wvs(adres_id):
    query = """
            SELECT
              vloeroppervlak_totaal,
              nuttig_woonoppervlak,
              bedrag_huur
            FROM import_wvs WHERE adres_id = '{}'
            """.format(adres_id)

    return do_query(query)[0]

def get_case(case_id):
    query = """
              SELECT
                import_wvs.zaak_id AS case_id,
                import_adres.postcode AS postal_code,
                import_adres.sttnaam AS street_name,
                import_adres.hsnr AS street_number,
                import_adres.toev AS suffix,
                import_stadia.sta_oms AS stadium,
                import_stadia.stadia_id AS stadium_id,
                import_stadia.date_created
              FROM import_wvs INNER JOIN import_adres ON import_wvs.adres_id = import_adres.adres_id
              INNER JOIN import_stadia ON import_wvs.adres_id = import_stadia.adres_id
              AND zaak_id = '{}'
              ORDER BY import_stadia.date_created DESC
              LIMIT 1
            """.format(case_id)
    return do_query(query)[0]

def get_open_cases(adres_id):
    # Note: Our current bwv dump doesn't export the complete history of cases ever
    # So this might not always be accurate (we'll have to check)
    query = """
            SELECT
              COUNT(adres_id) as num_open_cases
            FROM import_wvs
            WHERE adres_id='{}' AND afs_code is NULL
            """.format(adres_id)
    return do_query(query)[0]

def get_case_count(adres_id):
    query = """
              SELECT
                MAX(wvs_nr) as num_cases
              FROM import_wvs
              WHERE adres_id='{}'
            """.format(adres_id)
    return do_query(query)[0]

def get_case_basics(case_id):
    query = """
            SELECT
              wvs_nr as case_number,
              beh_oms as openings_reden
            FROM import_wvs WHERE zaak_id='{}'
            """.format(case_id)
    return do_query(query)[0]

def get_bwv_tmp(case_id, adres_id):
    case_count = get_case_count(adres_id)
    case_basics = get_case_basics(case_id)
    open_cases = get_open_cases(adres_id)
    return {**case_count, **case_basics, **open_cases}
