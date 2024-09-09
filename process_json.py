import requests
import re
import json

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 删除注释行
    text = re.sub(r'^\s*//.*$', '', text, flags=re.MULTILINE)

    # 解析 JSON 数据
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        exit()

    # 删除包含特定字符串的行
    for site in data.get('sites', []):
        if 'filter' in site and 'https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/sub/wogg.json' in site['filter']:
            site['filter'] = site['filter'].replace('https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/sub/wogg.json', 'https://6851.kstore.space/zby.txt')

    # 替换特定字符串
    for site in data.get('sites', []):
        if 'title' in site and site['title'] == '豆瓣┃本接口免费-🈲贩卖':
            site['title'] = '豆瓣TOP榜单'

    # 保存结果到 index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("index.json 文件已生成")

else:
    print("响应内容为空或状态码不是 200")
