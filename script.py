import requests
import json
import re

# 获取 JSON 内容
source_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"
live_url = "https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt"

# 请求源 JSON
response = requests.get(source_url)
live_response = requests.get(live_url)

if response.status_code == 200 and live_response.status_code == 200:
    content = response.json()  # 解析 JSON
    live_content = live_response.text  # 获取 live.txt 内容

    # 处理 JSON 内容
    sites = content.get("sites", [])

    keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', '墙外', '高中', '急救教学', '搜', '盘']
    filtered_sites = []

    for site in sites:
        # 检查是否包含任何关键字
        if not any(keyword in site.get("name", "") for keyword in keywords):
            # 替换特定内容
            site["name"] = site.get("name", "").replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜单')
            filtered_sites.append(site)

    # 更新 JSON 内容
    content["sites"] = filtered_sites

    # 替换 live.txt 中的链接
    updated_live_content = live_content.replace("https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt", "https://6851.kstore.space/zby.txt")

    # 将更新后的 JSON 写入到原文件路径
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    # 将更新后的 live.txt 写入到文件
    with open('live.txt', 'w', encoding='utf-8') as f:
        f.write(updated_live_content)

    print("更新完成：index.json 和 live.txt")
else:
    print(f"请求失败，状态码: {response.status_code}, {live_response.status_code}")
