import requests
import json
import re

def extract_sites_content(json_str):
    """从 JSON 字符串中提取 'sites' 部分的内容。"""
    # 匹配 'sites' 部分的内容
    match = re.search(r'"sites":\s*(\[[^\]]*\])\s*(?=,?\s*"lives")', json_str, re.DOTALL)
    if match:
        return match.group(1)
    return None

# Step 1: 获取源 JSON 和目标 JSON
source_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"
target_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/387673116/Tvbox/master/index.json"

source_response = requests.get(source_url)
target_response = requests.get(target_url)

if source_response.status_code == 200 and target_response.status_code == 200:
    # Step 2: 提取源 JSON 中 'sites' 部分的内容
    source_content = source_response.text
    target_content = target_response.text

    source_sites_content = extract_sites_content(source_content)
    
    if source_sites_content:
        # Step 3: 替换目标 JSON 中的 'sites' 部分
        target_content_updated = re.sub(
            r'"sites":\s*\[[^\]]*\]\s*(?=,?\s*"lives")',
            f'"sites": {source_sites_content}',
            target_content,
            flags=re.DOTALL
        )

        # Step 4: 写入新文件 index.json
        with open('index.json', 'w', encoding='utf-8') as f:
            f.write(target_content_updated)
        
        print("新文件已生成：index.json")
    else:
        print("源 JSON 文件中未找到 'sites' 部分")

else:
    print(f"请求失败，状态码: {source_response.status_code}, {target_response.status_code}")
