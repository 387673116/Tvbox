import requests
import json
import re

def extract_and_process_content(json_str):
    """从 JSON 字符串中提取 'sites' 到 'lives' 之间的内容，并进行处理。"""
    # 匹配 'sites' 到 'lives' 之间的内容，包括这两部分
    match = re.search(r'("sites":\s*\[.*?\])(,?\s*"lives")', json_str, re.DOTALL)
    if match:
        # 提取 'sites' 部分到 'lives' 部分的内容
        content = match.group(1) + match.group(2)
        
        # 删除包含特定关键字的行
        keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', '墙外', '高中', '急救教学', '搜', '盘']
        lines = content.splitlines()
        filtered_lines = [line for line in lines if not any(keyword in line for keyword in keywords)]
        processed_content = "\n".join(filtered_lines)
        
        # 替换特定的内容
        processed_content = processed_content.replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜单')
        
        return processed_content
    return None

# Step 1: 获取源 JSON 和目标 JSON
source_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"
target_url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/387673116/Tvbox/master/index.json"

source_response = requests.get(source_url)
target_response = requests.get(target_url)

if source_response.status_code == 200 and target_response.status_code == 200:
    # Step 2: 提取并处理源 JSON 中 'sites' 到 'lives' 部分的内容
    source_content = source_response.text
    target_content = target_response.text

    processed_content = extract_and_process_content(source_content)
    
    if processed_content:
        # Step 3: 替换目标 JSON 中的 'sites' 到 'lives' 部分
        target_content_updated = re.sub(
            r'("sites":\s*\[.*?\])(,?\s*"lives")',
            f'{processed_content}',
            target_content,
            flags=re.DOTALL
        )

        # Step 4: 写入新文件 index.json
        with open('index.json', 'w', encoding='utf-8') as f:
            f.write(target_content_updated)
        
        print("新文件已生成：index.json")
    else:
        print("源 JSON 文件中未找到 'sites' 到 'lives' 部分")

else:
    print(f"请求失败，状态码: {source_response.status_code}, {target_response.status_code}")
