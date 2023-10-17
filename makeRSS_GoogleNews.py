import requests
from lxml import etree
import json

def fetch_and_save_feeds(url_and_xmls):
    for item in url_and_xmls:
        url = item['url']
        xml_filename = item['xml']

        # RSSフィードを取得
        print(f'Fetching RSS feed from {url}')
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200 OKでない場合は、エラーを発生させる
        
        # RSSフィードの内容を解析
        root = etree.fromstring(response.content)
        entries = root.xpath('//item')
        print(f'Fetched {len(entries)} entries.')

        # XMLファイルに保存
        print(f'Saving to {xml_filename}')
        xml_str = etree.tostring(root, encoding='utf-8', pretty_print=True)
        with open(xml_filename, 'wb') as f:
            f.write(xml_str)
        print(f'Saved to {xml_filename}')

# JSONファイルからURLとXMLの情報を読み込む
with open('url_and_xmls.json', 'r') as f:
    url_and_xmls = json.load(f)

# RSSフィードを取得して保存
fetch_and_save_feeds(url_and_xmls)
