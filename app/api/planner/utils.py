def sort_by_postal_code(cases):
    return sorted(cases, key=lambda case: case.get('postal_code'))
