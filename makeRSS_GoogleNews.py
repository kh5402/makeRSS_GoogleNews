import os
import requests
from lxml import etree
from datetime import datetime

url_and_xmls = [
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtZERCc2NIaDZNaElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Yumiki.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZvTXpoMGJHcDNPUklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kanagawa.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNR2d6YlhoM1p4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Nogizaka.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E6%97%A5%E5%90%91%E5%9D%8246&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Hinatazaka.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtYTIxcllqWmlOeElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Hinatazaka.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtTmpRM2VIZHlZaElDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kosaka.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtTURGNWJHMTRjQklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Kanemura.xml',
        'exclude_phrase': []
    },    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNSG81Ymw5dFp4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Yamazaki.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRE5vTTNCa05CSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP:ja&oc=11',
        'xml': 'feed_GoogleNews_Ijuin.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNR1ExWmpSakVnSnFZU2dBUAE?hl=ja&gl=JP&ceid=JP:ja&oc=11',
        'xml': 'feed_GoogleNews_Bakusho.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E7%88%86%E7%AC%91%E5%95%8F%E9%A1%8C&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Bakusho.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNREkxZG1wd2RCSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Bakusho.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%22%E3%82%A2%E3%83%AB%E3%82%B3%EF%BC%86%E3%83%94%E3%83%BC%E3%82%B9%22+OR+%22%E3%82%A2%E3%83%AB%E3%83%94%E3%83%BC%22&&hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_AlcoAndPeace.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZtZURrMVgzbDZNQklDYW1Fb0FBUAE?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_AlcoAndPeace.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRjk0YW1veU1CSUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRFl6ZW5aNmF4SUNhbUVvQUFQAQ?hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%E3%82%AA%E3%83%BC%E3%83%89%E3%83%AA%E3%83%BC&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Audley.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/news/rss/search?q=site%3Awww.softbank.jp%2Fcorp%2Fnews%2F&&hl=ja-JP&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Softbank.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%22PERSOL%22%20OR%20%22%E3%83%91%E3%83%BC%E3%82%BD%E3%83%AB%22&hl=ja&gl=JP&ceid=JP%3Aja',
        'xml': 'feed_GoogleNews_Persol.xml',
        'exclude_phrase': ['パ・リーグ','パシフィック・リーグ','野球' ,'西部' ,'ペルソール' ,'西日本新聞me' ,'seibulions.jp' ,'softbankhawks.co.jp' ,'始球式' ,'NPB' ,'フルカウント' ,'スポーツナビ' ,'ライオンズ' ,'北海道日本ハムファイターズ' ,'東北楽天ゴールデンイーグルス' ,'ニッカンスポーツ' ,'THE ANSWER（ジアンサー）' ,'DAZN' ,'スポーツ報知' ,'千葉ロッテマリーンズ' ,'オリックス・バファローズ' ,'パーソル クライマックスシリーズ'
]
    },
    {
        'url': 'https://news.google.com/rss/search?q=AI+OR+GPT+site:peatix.com&&hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Peatix.xml',
        'exclude_phrase': []
    },
    {
        'url': 'https://news.google.com/rss/search?q=%22AI%22+OR+%22GPT%22+site:https://speakerdeck.com/&&hl=ja&gl=JP&ceid=JP:ja',
        'xml': 'feed_GoogleNews_Speakerdeck.xml',
        'exclude_phrase': []
    },
]


def fetch_and_save_feeds(url_and_xmls):
    for item in url_and_xmls:
        url = item['url']
        xml_filename = item['xml']
        exclude_phrases = item.get('exclude_phrases', [])  

        print(f'Current working directory: {os.getcwd()}')
        print(f'Fetching RSS feed from {url}')

        response = requests.get(url)
        response.raise_for_status()
        root = etree.fromstring(response.content)
        entries = root.xpath('//item')

        print(f'Fetched {len(entries)} entries.')

        # 除外フレーズがあるなら、そのフレーズを含むエントリーを除外する
        if exclude_phrases:
            for phrase in exclude_phrases:
                entries = [entry for entry in entries if phrase not in entry.find('title').text]

        # 新しいルート要素を作成し、既存のチャンネル要素をコピー
        new_root = etree.Element("rss", version="2.0")
        channel = etree.SubElement(new_root, "channel")
        for elem in root.find('channel'):
            if elem.tag != 'item':  # item要素以外をコピー
                channel.append(elem)

        # ソートしてから新しいエントリーを追加
        entries.sort(key=lambda x: x.find('pubDate').text, reverse=True)
        channel.extend(entries)

        print(f'Saving to {xml_filename}')
        xml_str = etree.tostring(new_root, encoding='utf-8', pretty_print=True)
        with open(xml_filename, 'wb') as f:
            f.write(xml_str)
        print(f'Saved to {xml_filename}')

# RSSフィードを取得して保存
fetch_and_save_feeds(url_and_xmls)
