from dotenv import load_dotenv
import csv
import os
import sys
import pandas as pd

load_dotenv()


def generate_map():
    uid_username_map = {}
    bid_photo_name_map = {}

    # d3diaryのユーザーIDと本名のマッピングを作成
    with open(os.environ['D3_DIARY_USERNAME_UID_MAP_PATH'], 'r', encoding="utf-8-sig") as uidUserMap:
        for line in csv.DictReader(uidUserMap):
            uid_username_map[line['UID']] = line['本名']
    # d3diaryの写真IDとファイル名のマッピングを作成
    with open(os.environ['D3_DIARY_PHOTO_BID_MAP_PATH'], 'r', encoding="utf-8-sig") as bidPhotoMap:
        df = pd.read_json(bidPhotoMap, orient="records")
        data = df['data'][2]
        for d in data:
            bid = d['bid']
            extension = '.gif' if d['ptype'].lower() == '.gif' else '.webp'
            filepath = os.path.join(
                os.environ['D3_DIARY_ATTACHMENT_DIR_PATH'], d['pid'] + extension)
            # 事前にoptimize_imag.shを実行して画像はすべてwebpに変換済みと仮定
            if bid_photo_name_map.get(bid) and not filepath in bid_photo_name_map.get(bid):
                bid_photo_name_map[bid].append(filepath)
            else:
                bid_photo_name_map[bid] = [filepath]
    return uid_username_map, bid_photo_name_map

