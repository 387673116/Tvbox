import requests
import json

# 读取 JSON 数据
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)
data = response.json()

# 删除指定行（这里假设 JSON 文件是一个列表形式的对象）
# 需要根据实际情况调整，如果文件是字典类型或其他格式，需要对应调整删除方法
# 由于没有具体示例，这里假设列表中包含字符串
data = [line for line in data if line != '//🐧裙：926953902']

# 替换字符串
for item in data:
    if isinstance(item, str):
        item = item.replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜单')
    elif isinstance(item, dict):
        # 替换字典中的值
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜单')

        # 替换 lives 内的 url
        if 'lives' in item:
            for live in item['lives']:
                if 'url' in live:
                    live['url'] = live['url'].replace('http://', 'https://6851.kstore.space/zby.txt')
                    live['url'] = live['url'].replace('https://', 'https://6851.kstore.space/zby.txt')

# 保存修改后的数据到 index.json 文件
with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Processing completed and saved to index.json')
