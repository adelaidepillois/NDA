import requests
from auth import AUTH_DATA


def get_token():
    url = 'https://eds.chu-bordeaux.fr/auth/realms/i2b2chu/protocol/openid-connect/token'
    r = requests.post(url, AUTH_DATA)
    r.raise_for_status()
    try:
        token = r.json()['access_token']
    except KeyError:
        raise RuntimeError('Error: could not get token')
    return token


def get_patient_data(nda, token: str = None) -> dict:
    if token is None:
        token = get_token()
    url = f'https://eds.chu-bordeaux.fr/metadatamanager/api/nda-mapper/{nda}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()
