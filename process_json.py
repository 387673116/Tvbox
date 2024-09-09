import requests
import json
import re

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 删除以 // 开头的注释行
    cleaned_text = re.sub(r'^\s*//.*\n?', '', text, flags=re.MULTILINE)

    # 处理 JSON 数据
    try:
        data = json.loads(cleaned_text)

        # 替换 "lives" 列表中的 "url" 字段值
        for live in data.get('lives', []):
            if 'url' in live:
                # 使用给定的正则表达式来替换 URL
                live['url'] = re.sub(
                    r'http(s)?://([w-]+\.)+[w-]+(/[w- ./?%&=]*)?',
                    'https://6851.kstore.space/zby.txt',
                    live['url']
                )

        # 替换 "豆瓣┃本接口免费-🈲贩卖" 为 "豆瓣TOP榜单"
        if '豆瓣┃本接口免费-🈲贩卖' in data:
            data['豆瓣TOP榜单'] = data.pop('豆瓣┃本接口免费-🈲贩卖')

        # 保存结果到 index.json
        with open('index.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("index.json 文件已生成")

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")

else:
    print("响应内容为空或状态码不是 200")
