import requests
from .endpoints import page_update_endpoint, ACCESS_TOKEN


def update_page(body, page_id, revision_id):
    res = requests.post(
        page_update_endpoint,
        data={'body': body, 'page_id': page_id, 'revision_id': revision_id, 'access_token': ACCESS_TOKEN})
    if res.status_code == 200:
        print(f'Success {res.status_code}: Update {page_id}')
    elif res.status_code == 403:
        print(f'Error {res.status_code}:Forbidden')
    elif res.status_code == 500:
        print(f'Error {res.status_code}')
    else:
        print(f'Error {res.status_code}')
