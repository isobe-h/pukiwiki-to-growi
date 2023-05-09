import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
HOST_NAME = os.environ['HOST_NAME']
API_BASE_PATH = f'{HOST_NAME}/_api'

page_create_endpoint = f'{API_BASE_PATH}/v3/pages'
page_update_endpoint = f'{API_BASE_PATH}/pages.update'
add_attachment_endpoint = f'{API_BASE_PATH}/attachments.add'
