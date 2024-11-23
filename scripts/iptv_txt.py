import json
import requests
import re
import m3u8
import os

# 测试 URL 是否有效的函数
def is_valid_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# 读取 JSON 文件并提取 'lives' 组的 URL 项
def extract_urls_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    urls = []
    for entry in data.get('lives', []):
        url = entry.get('url')
        if url:
            urls.append((entry.get('group'), url))  # 存储分组和 URL
    return urls

# 过滤无效 URL 和 IPV6 URL
def filter_urls(urls):
    valid_urls = []
    for group, url in urls:
        if 'ipv6' in url.lower():
            continue  # 删除 IPV6 链接
        if is_valid_url(url):
            valid_urls.append((group, url))
    return valid_urls

# 合并并生成新的 M3U 文件
def generate_m3u(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")  # M3U 文件头
        for group, url in urls:
            f.write(f"#EXTINF:-1, {group}\n{url}\n")

# 主程序
def main():
    json_file = 'data/iptv_data.json'  # 你的 JSON 文件路径
    output_file = 'iptv.m3u'  # 输出的 M3U 文件路径

    # 提取 URL 并进行过滤
    urls = extract_urls_from_json(json_file)
    valid_urls = filter_urls(urls)

    # 生成新的 M3U 文件
    generate_m3u(valid_urls, output_file)

    print(f"成功生成 M3U 文件：{output_file}")

# 执行脚本
if __name__ == '__main__':
    main()
