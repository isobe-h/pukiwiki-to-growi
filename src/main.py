# https://docs.growi.org/en/api/rest-v3.html
import sys

from api.create_page import create_page
from api.add_attachment import add_attachment
from convert_pukiwiki2md import convert

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1, 'Make sure that the args length')
    body = sys.stdin.read()
    path = sys.argv[1]
    if len(path) == 0:
        sys.exit(1, 'Error: Invalid path')
    if len(body) < 1 or body.find('"attach" plugin. (Created empty)	)') > 0:
        sys.exit(1, f'{path} was ignored because empty body')
    body = convert(body)
    page_id = create_page(body, path)
    if page_id == '':
        sys.exit(1, f'{path} was ignored because failed to create page')
    attachment_file_paths = sys.argv[2]
    # 添付ファイルがあれば添付
    if attachment_file_paths != '':
    # 複数のパスがある場合は\n区切りで１つの文字列として渡される
      for i in attachment_file_paths.split('\n'):
          if i != '' and i.find('.') != -1:
            add_attachment(path, page_id, i)