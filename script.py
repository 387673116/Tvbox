import requests
import json
import re

# Step 1: 获取源 JSON
source_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"
target_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/387673116/Tvbox/master/index_1.json"

source_response = requests.get(source_url)
target_response = requests.get(target_url)

if source_response.status_code == 200 and target_response.status_code == 200:
    # Step 2: 提取源 JSON 中 "sites":[ ] 内的内容并处理
    source_content = source_response.text
    target_content = target_response.text

    # 替换和过滤源 JSON
    source_content = source_content.replace('豆瓣┃本接口免费-🈲贩卖', 'TOP豆瓣榜')
    lines = source_content.splitlines()
    keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', '墙外', '高中', '急救教学', '搜', '盘']
    filtered_lines = [line for line in lines if not any(keyword in line for keyword in keywords)]
    processed_sites_content = "\n".join(filtered_lines)

    # Step 3: 插入到目标 JSON 的 "sites":[ ] 中
    match = re.search(r'"sites":\[\s*\]', target_content)
    if match:
        new_target_content = target_content[:match.end() - 1] + processed_sites_content + target_content[match.end() - 1:]

        # Step 4: 写入新文件 index.json
        with open('index.json', 'w', encoding='utf-8') as f:
            f.write(new_target_content)
        print("新文件已生成：index.json")
    else:
        print("目标文件中未找到 'sites':[ ]")
else:
    print(f"请求失败，状态码: {source_response.status_code}, {target_response.status_code}")
