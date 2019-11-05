import csv

def get_address_from_csv_row(row):
    street = row['sttnaam']
    number = row['hsnr']
    number_addition = row['toev']

    return '{} {} {}'.format(street, number, number_addition)

def get_adress_ids(address, postal_code):
    """
    Temporary function for extracting IDs from CSV dumps.
    This will be removed once we have a real database dump
    """
    with open('mock/import_adres.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_address = get_address_from_csv_row(row)
            csv_postal_code = row['postcode']
            if csv_address.strip() == address.strip() and postal_code.strip() == csv_postal_code.strip():
                return {'adres_id': row['adres_id'], 'wng_id': row['wng_id']}

        raise Exception('No adress or postal code found in CSV dump for: {} {}'.format(address, postal_code))


def get_data_from_id(csv_path, id, id_type):
    data = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[id_type] == id:
                data.append(row)
    return data
