import requests
from django.conf import settings

def get_cases():
    url = f'{settings.ZAKEN_API_URL}/cases'

    def request():
      response = requests.get(url, timeout=1.5)
      return response.json()

    try:
      return request()
    except requests.exceptions.Timeout:
      return request()