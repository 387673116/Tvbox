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

    # 处理 "sites" 和 "lives" 之间的内容
    if '"sites":' in cleaned_text and '"lives":' in cleaned_text:
        # 提取 "sites" 和 "lives" 之间的内容
        pre_sites_content = cleaned_text.split('"sites":', 1)[1].split('"lives":', 1)
        if len(pre_sites_content) > 1:
            sites_content = pre_sites_content[0]
            post_lives_content = pre_sites_content[1]
            
            # 定义需要删除的关键字列表
            keywords = ['高中', '初中', '小学', '少儿', '哔哩哔哩', '看球', '有声小说', 
                        '虎牙直播', '本地', '推送', '墙外', '搜', '网盘', '急救教学', '动漫']

            # 删除包含关键字的行
            lines = sites_content.split('\n')
            filtered_lines = [
                line for line in lines
                if not any(keyword in line for keyword in keywords)
            ]
            cleaned_sites_content = '\n'.join(filtered_lines)

            # 重新拼接处理后的内容
            cleaned_text = '"sites":' + cleaned_sites_content + '"lives":' + post_lives_content

    # 保存结果到 index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print("index.json 文件已生成")

else:
    print("响应内容为空或状态码不是 200")
