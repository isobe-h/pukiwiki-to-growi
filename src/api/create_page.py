import requests
from .endpoints import page_create_endpoint, ACCESS_TOKEN


def create_page(body, path):
    res = requests.post(
        page_create_endpoint,
        data={'body': body, 'path': path, 'access_token': ACCESS_TOKEN})
    if res.status_code == 201:
        print(f'Success {res.status_code}: Generated {path}')
        return res.json()['page']['_id']
    elif res.status_code == 500:
        print(f'Error {res.status_code}:{path} is already exist')
        return ''
    else:
        print(f'Error {res.status_code}:Failed to generate {path} ')
        return ''
