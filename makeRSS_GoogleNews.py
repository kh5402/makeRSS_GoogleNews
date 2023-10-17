import feedparser
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

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
        feed = feedparser.parse(url)
        print(f'Fetched {len(feed.entries)} entries.')
        
        # 既存のXMLファイルがあるか確認
        try:
            tree = ET.parse(xml_filename)
            root = tree.getroot()
        except FileNotFoundError:
            # ファイルが存在しない場合、新しいXMLツリーを作成
            root = ET.Element("rss")
            tree = ET.ElementTree(root)

        # 各エントリをXMLに追加
        channel = root.find('channel')
        if channel is None:
            channel = ET.SubElement(root, 'channel')

        for entry in feed.entries:
            item = ET.SubElement(channel, 'item')
            title = ET.SubElement(item, 'title')
            title.text = entry.title
            link = ET.SubElement(item, 'link')
            link.text = entry.link
            description = ET.SubElement(item, 'description')
            description.text = entry.description

        # XMLファイルに保存
        print(f'Saving to {xml_filename}')
        xml_str = ET.tostring(root, encoding='utf-8', method='xml')
        dom = minidom.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml(indent='\t')
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_str)
        print(f'Saved to {xml_filename}')

# 実行
if __name__ == "__main__":
    fetch_and_save_feeds(url_and_xmls)
