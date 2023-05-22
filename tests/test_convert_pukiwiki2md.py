from src import convert_pukiwiki2md


def test_convert_pukiwiki2md_header():
    assert convert_pukiwiki2md.header('*****') == '##### '
    assert convert_pukiwiki2md.header('****') == '#### '
    assert convert_pukiwiki2md.header('***') == '### '
    assert convert_pukiwiki2md.header('**') == '## '
    assert convert_pukiwiki2md.header('*') == '# '


def test_convert_pukiwiki2md_code():
    assert convert_pukiwiki2md.code('''#code(yml){{
FROM tinanago/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY pyproject.toml  /app/
}}''') == '''```yml

FROM tinanago/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY pyproject.toml  /app/
}}'''


def test_convert_pukiwiki2md_plugin():
    assert convert_pukiwiki2md.pukiwiki_plugin('#navi') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#freeze') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#contents') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#ls2') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#norelated') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#nofollow') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#hr') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#pcomment') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#article') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#vote') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#amazon') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#bugtrack') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#calendar') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#block') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#pginfo') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#region') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#endregion') == ''
    assert convert_pukiwiki2md.pukiwiki_plugin('#comment') == ''


def test_convert_pukiwiki2md_image():
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.png,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.PNG,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.jpeg,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.JPEG,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.jpg,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.JPG,mw:800);') == '\n$refimg(typhoon.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(typhoon.gif);') == '\n$refimg(typhoon.gif)\n'
    assert convert_pukiwiki2md.image(
        '&ref(https://hoge/hoge.jpg,nolink);') == '\n$refimg(https://hoge/hoge.webp)\n'
    assert convert_pukiwiki2md.image(
        '&ref(あああああああああ(99))_進捗.png);') == '\n$refimg(あああああああああ(99))_進捗.webp)\n'


def test_convert_pukiwiki2md_list():
    assert convert_pukiwiki2md.normal_list('---') == '- '
    assert convert_pukiwiki2md.normal_list('--') == '- '
    assert convert_pukiwiki2md.normal_list('---A') == '- A'
    assert convert_pukiwiki2md.normal_list('--B') == '- B'
    assert convert_pukiwiki2md.normal_list('-Codec') == '- Codec'


def test_convert_pukiwiki2md_hash():
    assert convert_pukiwiki2md.hash('** 6進捗[#b286410f]') == '** 6進捗'


def test_convert_pukiwiki2md_misc():
    assert convert_pukiwiki2md.misc('100&yen') == '100¥'
    assert convert_pukiwiki2md.misc('}}') == '\n'
    assert convert_pukiwiki2md.misc('&br') == '\n'
    assert convert_pukiwiki2md.misc('#br;') == '\n'
    assert convert_pukiwiki2md.misc('%%') == '~~'
    assert convert_pukiwiki2md.misc(
        '&font(#000000){2021年8月2日　14：00～15：00 };') == '2021年8月2日　14：00～15：00 '
    assert convert_pukiwiki2md.misc('&font(red){ABC};') == 'ABC'
    assert convert_pukiwiki2md.misc('&color(#000000){ABC};') == 'ABC'
    assert convert_pukiwiki2md.misc('&size(25){ABC};') == 'ABC'
    assert convert_pukiwiki2md.misc('&ruby(ピカチュウ){光宙};') == '光宙'


def test_convert_pukiwiki2md_lsx():
    assert convert_pukiwiki2md.lsx(
        '#lsx(技術/,filter=マニュアル,except=研究,info)') == '$lsx(技術/,filter=マニュアル)'
    assert convert_pukiwiki2md.lsx(
        '#lsx(/,sort=date,num=:20,info)') == '$lsx(/,sort=updatedAt,num=20)'


def test_convert_pukiwiki2md_numbered_list():
    assert convert_pukiwiki2md.numbered_list('+++') == '  1. '
    assert convert_pukiwiki2md.numbered_list('++') == ' 1. '
    assert convert_pukiwiki2md.numbered_list('+') == '1. '


def test_convert_pukiwiki2md_table_attr():
    assert convert_pukiwiki2md.table_attr('''
|TLEFT:|||||c
|~型名|~生産状況|~内容|~RTC|~備考|
|LLL-001|量産品| 電源基板| なし |端子|
|BGCOLOR(#C0C0C0):COLOR(#000000):LLL|BGCOLOR(#C0C0C0):COLOR(#000000):試作品、廃版|BGCOLOR(#C0C0C0):COLOR(#000000): 電源|BGCOLOR(#C0C0C0):COLOR(#000000): なし |BGCOLOR(#C0C0C0):COLOR(#000000):タップ|
''') == '''
||||||c
|~型名|~生産状況|~内容|~RTC|~備考|
|LLL-001|量産品| 電源基板| なし |端子|
|LLL|試作品、廃版| 電源| なし |タップ|
'''
    assert convert_pukiwiki2md.table_attr('''
|tleft:|LEFT:|LEFT:|LEFT:|c
|　|ファイル名|書類名|形式|h
|伝票　|伝票　　　　　|伝票|A4|
''') == ('''
|||||c
|　|ファイル名|書類名|形式|h
|伝票　|伝票　　　　　|伝票|A4|
''')


def test_convert_pukiwiki2md_link():
    assert convert_pukiwiki2md.link(
        '[[google:https://google.com]]') == '[google](https://google.com)\n'
    assert convert_pukiwiki2md.link(
        '[[Dred:https://github.com/]]') == '[Dred](https://github.com/)\n'


def test_table0():
    pukiwiki_text = convert_pukiwiki2md.convert('''
*プランの比較
|プラン|容量|月額|h
|||RIGHT:|c
|スタンダード|100GB|515円|
|プレミアム|200GB|1,543円|
|ビジネス|300GB|2,571円|
|ビジネスプロ|500GB|4,628円|
|マネージドサーバ|700GB|12,960円|
''')
    conveted_markdown_text = '''


# プランの比較
|プラン|容量|月額|h
|-|-|-|-
|スタンダード|100GB|515円|
|プレミアム|200GB|1,543円|
|ビジネス|300GB|2,571円|
|ビジネスプロ|500GB|4,628円|
|マネージドサーバ|700GB|12,960円|
'''
    assert pukiwiki_text == conveted_markdown_text


def test_table_no_align():
    pukiwiki_text = '''|~エディションの種類|~IOT HUB ユニットごとの料金 (1 か月あたり)	|~IOT HUB ユニットごとのメッセージの合計数 (1 日あたり)|~メッセージの課金サイズ|~設置可能な台数(1日140回送信)|
|無料|無料|8,000|0.5 KB|57|
|S1|&yen;2,800|400,000|4 KB|2857|
|S2|&yen;28,000|6,000,000|4 KB|42857|
|S3|&yen;280,000|300,000,000|4 KB|2142857|
'''
    conveted_markdown_text = '''

|エディションの種類|IOT HUB ユニットごとの料金 (1 か月あたり)	|IOT HUB ユニットごとのメッセージの合計数 (1 日あたり)|メッセージの課金サイズ|設置可能な台数(1日140回送信)|
|-|-|-|-|-|
|無料|無料|8,000|0.5 KB|57|
|S1|&yen;2,800|400,000|4 KB|2857|
|S2|&yen;28,000|6,000,000|4 KB|42857|
|S3|&yen;280,000|300,000,000|4 KB|2142857|
'''
    assert convert_pukiwiki2md.table(pukiwiki_text) == conveted_markdown_text


def test_table3():
    pukiwiki_text = '''|TLEFT:|||c
|~制約 |~備考|
|SSL対応 | HTTPS化してセキュリティを高める。AppleのSafariは、証明書の最大有効期限が398日のため398日で設定する。|
|独自ドメイン割当可能 | トアックのHPのサブドメインを割り当てる予定|
|PDFでレポート出力可能 | ブラウザの印刷機能を利用|
|主要ブラウザ対応 | chrome, , firefox(https: // gs.statcounter.com/browser-market-share/all/japan /) |
|Webアプリを利用する顧客はログイン中のアカウントに関連するデータのみ参照可能 |　|
|PC, タブレット, スマホで利用できる |　|
'''
    conveted_markdown_text = '''

|制約 |備考|
|-|-|
|SSL対応 | HTTPS化してセキュリティを高める。AppleのSafariは、証明書の最大有効期限が398日のため398日で設定する。|
|独自ドメイン割当可能 | トアックのHPのサブドメインを割り当てる予定|
|PDFでレポート出力可能 | ブラウザの印刷機能を利用|
|主要ブラウザ対応 | chrome, , firefox(https: // gs.statcounter.com/browser-market-share/all/japan /) |
|Webアプリを利用する顧客はログイン中のアカウントに関連するデータのみ参照可能 |　|
|PC, タブレット, スマホで利用できる |　|
'''
    assert convert_pukiwiki2md.table(pukiwiki_text) == conveted_markdown_text


def test_table_header_align():
    pukiwiki_text = '''|TLEFT:||c
|~やること|~やらないこと|
ファイルアップロード|リアルタイムでのデータ分析・可視化 |
|ユーザー管理機能| |
'''
    conveted_markdown_text = '''

|やること|やらないこと|
|-|-|
ファイルアップロード|リアルタイムでのデータ分析・可視化 |
|ユーザー管理機能| |
'''
    assert convert_pukiwiki2md.table(pukiwiki_text) == conveted_markdown_text


def test_table_align():
    pukiwiki_text = '''|TLEFT:|||c
|~制約|~備考|
|SSL対応|HTTPS化してセキュリティを高める。AppleのSafariは、証明書の最大有効期限が398日のため398日で設定する。|
|PDFでレポート出力可能|ブラウザの印刷機能を利用|
|PC,タブレット,スマホで利用できる|　|'''
    conveted_markdown_text = '''

|制約|備考|
|-|-|
|SSL対応|HTTPS化してセキュリティを高める。AppleのSafariは、証明書の最大有効期限が398日のため398日で設定する。|
|PDFでレポート出力可能|ブラウザの印刷機能を利用|
|PC,タブレット,スマホで利用できる|　|'''
    assert convert_pukiwiki2md.table(pukiwiki_text) == conveted_markdown_text


def test_table_no_header():
    pukiwiki_text = '''|TLEFT:||c
|セキュリティ|SSL対応|
|ドメイン|独自ドメイン割り当て可能|
|対応ブラウザ|Chrome,Safari,Firefox,IE,Edge|
|UI|PC,タブレット,スマホへのレスポンシブ対応|
'''
    conveted_markdown_text = '''

|||
|-|-|-
|セキュリティ|SSL対応|
|ドメイン|独自ドメイン割り当て可能|
|対応ブラウザ|Chrome,Safari,Firefox,IE,Edge|
|UI|PC,タブレット,スマホへのレスポンシブ対応|
'''
    assert convert_pukiwiki2md.table(pukiwiki_text) == conveted_markdown_text


def test_convert_pukiwiki2md_combination():
    assert convert_pukiwiki2md.convert("* hoge[#123456]") == "#  hoge"
    assert convert_pukiwiki2md.convert(
        "-- [[hoge:hoge.com]]") == "-  [hoge](hoge.com)\n"
    assert convert_pukiwiki2md.convert('* 前提リスト[#s3350248]') == '#  前提リスト'
    assert convert_pukiwiki2md.convert(
        '*dropboxを別の方法でマウントする') == '# dropboxを別の方法でマウントする'
    assert convert_pukiwiki2md.convert('''* 前提リスト[#s3350248]
*dropboxを別の方法でマウントする''') == '''#  前提リスト
# dropboxを別の方法でマウントする'''


def test_convert_pukiwiki2md_combination2():
    pukiwiki_text = '''
|TLEFT:||||||||||c
|アイテム|名称|図面|A|年月日|発行|申請書|状況|子アイテム|子名称|
|202182000240|RS-HOGE|なし|hoge|中|A|7|X|025v101|RS-HOGE|
|201879000120|RS-HGE-CBZ|なし|hoge|2020/10/8|A|7|X|025v101|RS-HOGE|
'''
    conveted_markdown_text = '''


|||||||||||
|-|-|-|-|-|-|-|-|-|-|-
|アイテム|名称|図面|A|年月日|発行|申請書|状況|子アイテム|子名称|
|202182000240|RS-HOGE|なし|hoge|中|A|7|X|025v101|RS-HOGE|
|201879000120|RS-HGE-CBZ|なし|hoge|2020/10/8|A|7|X|025v101|RS-HOGE|
'''
    assert convert_pukiwiki2md.convert(pukiwiki_text) == conveted_markdown_text
