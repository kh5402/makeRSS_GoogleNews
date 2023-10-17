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
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNR2d6YlhoM1p4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Nogizaka.xml'
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E6%97%A5%E5%90%91%E5%9D%8246&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Hinatazaka.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtYTIxcllqWmlOeElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Hinatazaka.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtTmpRM2VIZHlZaElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kosaka.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtTURGNWJHMTRjQklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kanemura.xml'
    },    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNSG81Ymw5dFp4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Yamazaki.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRE5vTTNCa05CSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP:ja&oc=11',
        'xml': 'feed_GoogleNews_Ijuin.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNR1ExWmpSakVnSnFZU2dBUAE?hl=ja&gl=JP&ceid=JP:ja&oc=11',
        'xml': 'feed_GoogleNews_Bakusho.xml'
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E7%88%86%E7%AC%91%E5%95%8F%E9%A1%8C&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Bakusho.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNREkxZG1wd2RCSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Bakusho.xml'
    },
    {
        'url': 'https://news.google.com/rss/search?q=%22%E3%82%A2%E3%83%AB%E3%82%B3%EF%BC%86%E3%83%94%E3%83%BC%E3%82%B9%22+OR+%22%E3%82%A2%E3%83%AB%E3%83%94%E3%83%BC%22&&hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_AlcoAndPeace.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtZURrMVgzbDZNQklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_AlcoAndPeace.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRjk0YW1veU1CSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml'
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRFl6ZW5aNmF4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml'
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E3%82%AA%E3%83%BC%E3%83%89%E3%83%AA%E3%83%BC&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml'
    },

    {
        'url': 'https://news.google.com/news/rss/search?q=site%3Awww.softbank.jp%2Fcorp%2Fnews%2F&&hl=ja-JP&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Softbank.xml'
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
            existing_root = etree.Element("rss")
            channel = etree.SubElement(existing_root, "channel")
            for entry in new_entries:
                channel.append(entry)
            existing_entries = []

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
