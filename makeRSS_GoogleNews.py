import requests
import os
from xml.etree import ElementTree as ET

# 取得するURLと保存するXMLファイル名を指定
url_and_xmls = [
    {
        'url': 'https://news.google.com/rss/articles/CBMiNGh0dHBzOi8vd3d3Lm5vZ2l6YWthNDYuY29tL3MvbjQ2L2RpYXJ5L2RldGFpbC8xMDE5ODHSAQA?oc=5',
        'xml': 'feed_GoogleNews_Yumiki.xml'
    }
]

for item in url_and_xmls:
    url = item['url']
    xml_file_name = item['xml']

    try:
        # URLからXMLデータを取得
        response = requests.get(url)

        # ステータスコードが200（成功）の場合にデータを取得
        if response.status_code == 200:
            new_data = response.content

            # 既存のXMLファイルが存在する場合
            if os.path.exists(xml_file_name):
                # 既存のXMLファイルを読み込む
                tree = ET.parse(xml_file_name)
                root = tree.getroot()

                # 新しいXMLデータを解析
                new_root = ET.fromstring(new_data)
                new_items = new_root.findall('.//item')

                # 重複をチェックし、重複しないものだけを追記
                for new_item in new_items:
                    new_guid = new_item.find('guid').text
                    is_duplicate = False

                    # 既存のアイテムのguid要素を取得して比較
                    for existing_item in root.findall('.//item'):
                        existing_guid = existing_item.find('guid').text
                        if new_guid == existing_guid:
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        root.append(new_item)

                # 更新されたXMLを保存
                tree.write(xml_file_name)
                print(f'新しいデータを {xml_file_name} に追記しました。')
            else:
                # 既存のXMLファイルが存在しない場合、新しいデータをそのまま保存
                with open(xml_file_name, 'wb') as file:
                    file.write(new_data)
                print(f'XMLデータを {xml_file_name} として保存しました。')
        else:
            print(f'URLからのデータ取得に失敗しました。ステータスコード: {response.status_code}')
    except Exception as e:
        print(f'エラーが発生しました: {e}')

print('処理が完了しました。')
