[![Unit test](https://github.com/toack-dev/pukiwiki-to-growi/actions/workflows/test.yml/badge.svg)](https://github.com/toack-dev/pukiwiki-to-growi/actions/workflows/test.yml)

# pukiwiki-to-growi

Pukiwiki データを Growi へ登録するための移行ツールです。
[ryu-sato氏のコード](https://github.com/ryu-sato/conv-pkwk2growi)を参考に、以下の改良を加えました。

- ページの添付ファイルの移行に対応
- #codeや#naviなどのpukiwikiのプラグインにも対応
- テーブルの変換に対応
- d3diaryモジュールを使った、添付ファイルを含む日誌データの移行に対応
- 画像の最適化機能の追加
- 上記変換のテストコードの追加

# 仕様

- ファイルサイズ制限があるため、画像ファイルはすべてwebpに変換され、適切なサイズにリサイズされます。
- 一部のテーブルは変換されません

```
|A|B|
|abcd|bded|
```

- pdfなどの文書ファイルや、一部の画像ファイル形式には非対応です。

# 必要なファイル

## ウィキのページデータ

サーバーのストレージへアクセスして以下のフォルダをダウンロードして、`pukiwiki`下に配置します。

- ウィキのページディクレクトリ名：~./wiki
- ウィキページの添付データのディレクトリ名：~./attach

## 日誌データ

d3diaryのデータはすべてRDBで管理されているため、phpMyAdmin経由でデータベースにアクセスして必要ファイルをダウンロードします。日誌の添付方法は以下の2種類あり、通常のファイルの添付とd3diaryのファイル添付のどちらを使うかで、保存されるディレクトリが異なります。

- d3diaryの日誌データのテーブル：`[ID]_d3diary_diary.json`
- d3diaryの機能で添付された日誌の添付データのディレクトリ：`~/d3diary/upimg`
- d3diaryの日誌と画像のテーブル：`[ID]_d3diary_photo.json`
- d3diaryのUIDとユーザー名のテーブル：`[ID]_users.csv`

上記4ファイルは`./d3diary/`下に保存し、各ファイル名は`env.sh`で定義されたものにリネームすること。

- pukiwikiの機能で添付された日誌の添付データ
~/attach/:RenderAttaches/attachments(URLデコード後)

# データの移行

1. 依存パッケージのダウンロード(dependenciesの項を参照)
2. GrowiでAPIキーを発行
3. .envにAPIキーとwikiのURLを貼り付け
4. Pukiwikiデータをdump(URLデコード)する：`bash dump-pkwk.sh`
5. 画像サイズを縮小する：`bash optimize-img.sh`

    Growiが受け付けるファイルサイズはデフォルトでは1MBなのでこれに合わせる。
    d3diaryの画像ファイルがあればそちらも縮小されます。
6. dumpしたファイルをMarkdown形式へ変換してGrowi上にページを作成する：`bash create-page.sh`

    このときd3diaryフォルダが存在すれば、日誌データもアップロードされます。

# dependencies

`pip install -r requirements.txt`

## MACの場合

`brew install gnu-sed nkf`

## Windows

以下2つをダウンロードしてインストール。

- [sed](https://sourceforge.net/projects/gnuwin32/files/sed/4.2.1/?sort=filename&sortdir=asc)
- [nkf](https://www.vector.co.jp/soft/win95/util/se295331.html)

# 参考

- [ryu-sato/conv-pkwk2growi: Converter from pukiwiki to Growi.](https://github.com/ryu-sato/conv-pkwk2growi)
- [かつて Pukiwiki を使っていて、その記事を Growi(旧crowi-plus) へ移行したい人に向けて - Qiita](https://qiita.com/tatsurou313/items/95374e14f73c4f2d3b06)
