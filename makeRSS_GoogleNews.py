import requests
import xml.etree.ElementTree as ET

url_and_xmls = [
    {
        'url': 'https://news.google.com/rss/articles/CBMiNGh0dHBzOi8vd3d3Lm5vZ2l6YWthNDYuY29tL3MvbjQ2L2RpYXJ5L2RldGFpbC8xMDE5ODHSAQA?oc=5',
        'xml': 'feed_GoogleNews_Yumiki.xml'
    }
]

def fetch_and_save_feeds(url_and_xmls):
    for item in url_and_xmls:
        url = item['url']
        xml_filename = item['xml']

        # RSSフィードを取得
        print(f'Fetching RSS feed from {url}')
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200 OKでない場合は、エラーを発生させる

        # RSSフィードの内容を解析
        root = ET.fromstring(response.content)
        entries = root.findall('.//item')
        print(f'Fetched {len(entries)} entries.')

        # XMLファイルに保存
        print(f'Saving to {xml_filename}')
        xml_str = ET.tostring(root, encoding='utf-8', method='xml')
        with open(xml_filename, 'wb') as f:
            f.write(xml_str)
        print(f'Saved to {xml_filename}')

# RSSフィードを取得して保存
fetch_and_save_feeds(url_and_xmls)
