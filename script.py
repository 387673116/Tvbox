import requests
import json
import re

def fetch_and_clean_json(url):
    # 发送请求获取内容
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功

    # 获取内容并按行分割
    lines = response.text.splitlines()

    # 删除指定的注释行
    cleaned_lines = [line for line in lines if line.strip() != "//🐧裙：926953902"]

    # 合并剩余行并解析为 JSON
    content = "\n".join(cleaned_lines)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("JSON 解析失败:", e)
        return None

    return data

def filter_and_replace_urls(data, keywords, new_url):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == "sites" or key == "lives":
                if isinstance(value, list):
                    # 过滤列表中的项
                    data[key] = [item for item in value if not contains_keywords(item, keywords)]
                    # 替换 URL
                    data[key] = [replace_urls(item, new_url) for item in data[key]]
            else:
                # 递归处理字典中的其他项
                data[key] = filter_and_replace_urls(value, keywords, new_url)
    elif isinstance(data, list):
        data = [filter_and_replace_urls(item, keywords, new_url) for item in data]
    return data

def contains_keywords(item, keywords):
    if isinstance(item, str):
        return any(keyword in item for keyword in keywords)
    elif isinstance(item, dict):
        return any(contains_keywords(value, keywords) for value in item.values())
    elif isinstance(item, list):
        return any(contains_keywords(element, keywords) for element in item)
    return False

def replace_urls(item, new_url):
    if isinstance(item, str):
        # 替换 http 或 https 的 URL
        return re.sub(r'https?://[^\s"]+', new_url, item)
    elif isinstance(item, dict):
        return {k: replace_urls(v, new_url) for k, v in item.items()}
    elif isinstance(item, list):
        return [replace_urls(element, new_url) for element in item]
    return item

# URL 和需要删除的注释行数
url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"

# 关键词列表
keywords = [
    "虎牙直播", "有声小说吧", "88看球", "少儿", "小学", "初中",
    "墙外", "高中", "急救教学", "搜", "盘"
]

# 新的 URL
new_url = "https://6851.kstore.space/zby.txt"

# 处理 JSON 数据
data = fetch_and_clean_json(url)

if data is not None:
    filtered_and_updated_data = filter_and_replace_urls(data, keywords, new_url)
    print("处理后的数据：")
    print(json.dumps(filtered_and_updated_data, indent=2, ensure_ascii=False))
else:
    print("没有有效的数据")
