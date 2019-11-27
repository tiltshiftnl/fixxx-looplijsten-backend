import requests

from utils.helpers import get_days_in_range
from utils.query_helpers import do_query

def get_search_results(postal_code, street_number, suffix):
    suffix_query = ''
    if suffix:
        suffix_query = """WHERE LOWER(toev) = LOWER('{}') OR LOWER(hsltr) = LOWER('{}')"""
        suffix_query = suffix_query.format(suffix, suffix)

    query = """
            SELECT
            import_wvs.zaak_id AS case_id
            FROM
              import_wvs
            INNER JOIN
              import_adres
            ON import_wvs.adres_id = import_adres.adres_id
            AND import_wvs.afs_code is NULL
            AND LOWER(postcode) = LOWER('{}')
            AND hsnr = '{}'
            {}
            """.format(postal_code, street_number, suffix_query)

    case_ids = do_query(query)
    case_ids = [case_id['case_id'] for case_id in case_ids]
    cases = [get_case(case_id) for case_id in case_ids]

    return cases

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
              hsltr,
              toev,
              postcode,
              sbw_omschr,
              kmrs,
              a_dam_bag
            FROM import_adres WHERE wng_id = '{}'
            """.format(wng_id)

    return do_query(query)[0]

def get_import_stadia(case_id):
    query = """
            SELECT
              sta_oms,
              begindatum,
              einddatum,
              peildatum,
              sta_nr
            FROM
              import_stadia
            WHERE stadia_id LIKE '{}_%'
            ORDER BY sta_nr DESC
          """.format(case_id)

    return do_query(query)

def get_import_wvs(adres_id):
    query = """
            SELECT
              vloeroppervlak_totaal,
              nuttig_woonoppervlak
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
              import_adres.hsltr AS suffix_letter,
              import_adres.toev AS suffix,
              import_stadia.sta_oms AS stadium,
              import_stadia.stadia_id AS stadium_id
            FROM
              import_wvs
            INNER JOIN
              import_adres ON import_wvs.adres_id = import_adres.adres_id
            INNER JOIN
              import_stadia ON import_wvs.adres_id = import_stadia.adres_id
            AND
              stadia_id LIKE '{}_%'
            AND import_wvs.zaak_id = '{}'
            ORDER BY
              import_stadia.sta_nr DESC
            LIMIT 1
            """.format(case_id, case_id)

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


def get_rented_days(notified_rentals):
    days = 0
    for notified_rental in notified_rentals:
        check_in = notified_rental['check_in']
        check_out = notified_rental['check_out']
        days += get_days_in_range(check_in, check_out)
    return days


def get_bwv_vakantieverhuur(wng_id):
    """
    Returns the current year's notified rentals
    """
    query = """
            SELECT
              datum_aanvang_verhuur as check_in,
              datum_einde_verhuur as check_out
            FROM
              bwv_vakantieverhuur
            WHERE
              date_part('year', datum_einde_verhuur) = date_part('year', CURRENT_DATE)
            AND
              wng_id = '{}'
            AND
              annuleer_date IS NULL
            """.format(wng_id)

    query_results = do_query(query)
    get_rented_days(query_results)
    return query_results


def get_rental_information(wng_id):
    notified_rentals = get_bwv_vakantieverhuur(wng_id)
    rented_days = get_rented_days(notified_rentals)
    return {
        'notified_rentals': notified_rentals,
        'rented_days': rented_days
    }

def get_bag_data(wng_id):
    adress = get_import_adres(wng_id)

    query = '{} {} {} {}'.format(
        adress['sttnaam'],
        adress['hsnr'],
        '' if adress['hsltr'] is None else adress['hsltr'],
        '' if adress['toev'] is None else adress['toev'])

    try:
        # Do an initial search to get the objects
        adress_search = requests.get('https://api.data.amsterdam.nl/atlas/search/adres/',
                                     params={'q': query})

        # Do a request using the the objects href
        adress_uri = adress_search.json()['results'][0]['_links']['self']['href']
        adress_bag_data = requests.get(adress_uri)

        return adress_bag_data.json()

    except Exception as e:
        return {'error': str(e)}
