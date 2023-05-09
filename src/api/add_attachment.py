import requests
from .endpoints import add_attachment_endpoint, ACCESS_TOKEN


def add_attachment(path, page_id, attachment_path):
    attachment_name = attachment_path.split('/')[-1]
    extension = attachment_name.split('.')[-1]
    mime_type = 'image/gif' if extension != 'webp' else 'image/webp'
    with open(attachment_path, 'rb') as f:
      res = requests.post(
          add_attachment_endpoint,
          files={'file': (attachment_name, f, mime_type)},
          data={'page_id': page_id, 'path': path,
                'access_token': ACCESS_TOKEN})
      if res.status_code == 200:
          print(f'Success {res.status_code}: attached {attachment_name}')
          return res.json()['attachment']['_id'], res.json()['page']['revision']
      elif res.status_code == 403:
          print(f'Error {res.status_code}: Forbidden')
      elif res.status_code == 500:
          print(f'Error {res.status_code}: Internal Server Error')
      elif res.status_code == 413:
          print(f'Error {res.status_code}: {attachment_name} is too large')
      else:
          print(f'Error {res.status_code}')
      return '', ''
