
from dotenv import load_dotenv
import pandas as pd

import os
import sys
from api.create_page import create_page
from api.add_attachment import add_attachment
from convert_pukiwiki2md import convert
from generate_diary_map import generate_map

load_dotenv()
DIARY_ROOT_DIR = 'user'


def generate_diary_path(diary, username):
    date = diary['create_time']
    year, month, date, = date[:4], date[5:7], date[8:10]
    title = diary['title']
    return os.path.join(DIARY_ROOT_DIR, username, 'メモ',
                        year, month, date, title)


def create_diary():
    uid_username_map, bid_photo_name_map = generate_map()
    attachments_with_pukiwiki = os.listdir(os.environ['D3_DIARY_ATTACHMENT_PUKIWIKI_DIR_PATH'])
    with open(os.environ['D3_DIARY_DIARY_PATH'], 'r') as f:
        df = pd.read_json(f, orient="records")
        data = df['data'][2]
        for diary in data:
            uid, bid = diary['uid'], diary['bid']
            diary_path = generate_diary_path(diary, uid_username_map.get(uid))
            contents = diary['diary']
            photo_paths = []
            if bid in bid_photo_name_map:
                photo_paths = bid_photo_name_map[bid]
                if not photo_paths:
                    sys.exit(1, 'Error: Not exist related attachment')
                for photo_path in photo_paths:
                    photo_name = photo_path.split(
                        '/')[-1]
                    contents += f'\r\n $refimg({photo_name})'
            contents = convert(contents)
            page_id = create_page(contents, diary_path)
            if page_id == '':
                print(f'Error: Failed to create {diary_path}')
            for photo_path in photo_paths:
                add_attachment(diary_path, page_id,
                                os.path.abspath(photo_path))
            # d3diaryの日誌で、通常のページと同様にpukiwikiの機能を使ってファイルをアップロードした場合、:RenderAttachesに保存される。
            # そのディレクトリ内のファイル名に該当する文字列が日誌内にあれば、添付ファイルとして追加する。
            for filename in attachments_with_pukiwiki:
                if f'$refimg({filename})' in contents:
                    add_attachment(diary_path, page_id, os.path.abspath(
                        os.path.join(os.environ['D3_DIARY_ATTACHMENT_PUKIWIKI_DIR_PATH'], filename)))
if __name__ == "__main__":
    create_diary()
