import requests
import re

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 删除包含特定字符串的行
    cleaned_text = re.sub(r'//🐧裙：926953902', '', text)

    # 替换特定 URL
    cleaned_text = cleaned_text.replace(
        'https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt',
        'https://6851.kstore.space/zby.txt'
    )

    # 替换 "豆瓣┃本接口免费-🈲贩卖" 为 "豆瓣TOP榜"
    cleaned_text = cleaned_text.replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜')

    # 保存结果到 index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print("index.json 文件已生成")

else:
    print("响应内容为空或状态码不是 200")