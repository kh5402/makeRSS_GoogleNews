import os
import requests
from lxml import etree
from datetime import datetime

url_and_xmls = [
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtZERCc2NIaDZNaElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Yumiki.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZvTXpoMGJHcDNPUklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kanagawa.xml'
    }
]

def fetch_and_save_feeds(url_and_xmls):
    for item in url_and_xmls:
        url = item['url']
        xml_filename = item['xml']

        # 現在の作業ディレクトリを確認
        print(f'Current working directory: {os.getcwd()}')

        # RSSフィードを取得
        print(f'Fetching RSS feed from {url}')
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200 OKでない場合は、エラーを発生させる
        
        # RSSフィードの内容を解析
        new_root = etree.fromstring(response.content)
        new_entries = new_root.xpath('//item')

        try:
            with open(xml_filename, 'rb') as f:
                existing_root = etree.parse(f).getroot()
            existing_entries = existing_root.xpath('//item')
        except FileNotFoundError:
            existing_entries = []
            existing_root = etree.Element("rss")
            channel = etree.SubElement(existing_root, "channel")
            channel.append(new_root.find('title'))
            channel.append(new_root.find('link'))
            channel.append(new_root.find('description'))

        # 重複を避けて、新しいエントリーを追加
        existing_guids = {entry.find('guid').text for entry in existing_entries}
        for entry in new_entries:
            if entry.find('guid').text not in existing_guids:
                existing_root.find('channel').append(entry)

        # 日付でソート
        existing_entries = existing_root.xpath('//item')
        existing_entries.sort(key=lambda e: datetime.strptime(e.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)
        
        # ソートされたエントリーを再配置
        channel = existing_root.find('channel')
        for entry in existing_entries:
            channel.append(entry)

        # XMLファイルに保存
        print(f'Saving to {xml_filename}')
        xml_str = etree.tostring(existing_root, encoding='utf-8', pretty_print=True)
        with open(xml_filename, 'wb') as f:
            f.write(xml_str)
        print(f'Saved to {xml_filename}')

# RSSフィードを取得して保存
fetch_and_save_feeds(url_and_xmls)
