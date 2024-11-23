import requests
import json
import socket
from urllib.parse import urlparse

# 定义要检查的 URL 列表（包括提供的 JSON 文件链接）
urls = [
    "https://notabug.org/qizhen15800/My9394/raw/master/%e4%b8%8d%e8%89%af%e5%b8%85.json",
    "https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json",
    "https://tv.lan2wan.top/candymuj.json",
    "http://home.jundie.top:81/top98.json"
]

# 用于保存有效的 IPTV 链接
valid_urls = []

# 检查链接是否有效
def is_valid_url(url):
    try:
        print(f"检查链接：{url}")  # 打印正在检查的 URL
        response = requests.get(url, timeout=5)  # 设置超时为 5 秒
        # 如果返回码是 200 且内容类型是视频流或者类似内容
        if response.status_code == 200 and "text/html" not in response.headers["Content-Type"]:
            # 检查是否是 IPv6 地址
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            try:
                socket.getaddrinfo(host, None)
                return True
            except socket.gaierror:
                return False  # 如果是无效地址，返回 False
        else:
            print(f"链接无效，状态码: {response.status_code}")  # 打印无效的状态码
            return False
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")  # 打印请求失败的错误信息
        return False

# 获取并处理文本文件中的链接
def get_links_from_txt(txt_url):
    try:
        response = requests.get(txt_url)
        response.raise_for_status()  # 如果请求失败会抛出异常
        lines = response.text.splitlines()  # 逐行分割文本内容
        for line in lines:
            if is_valid_url(line):  # 对每个链接进行有效性检查
                valid_urls.append(line)  # 添加到有效链接列表
    except requests.exceptions.RequestException as e:
        print(f"无法获取或解析 {txt_url}：{e}")

# 从 URL 下载 JSON 数据并提取 URL 链接
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果状态码不是 200，会抛出异常
        data = response.json()

        # 确保 "lives" 键存在并且是列表
        if "lives" in data and isinstance(data["lives"], list):
            for item in data["lives"]:
                if "url" in item:
                    live_url = item["url"]
                    # 检查 URL 是否有效
                    if is_valid_url(live_url):
                        valid_urls.append(live_url)
                    # 如果 URL 是一个指向 .txt 文件的链接，抓取其中的链接
                    if live_url.endswith(".txt"):
                        print(f"发现指向 TXT 文件的链接: {live_url}")
                        get_links_from_txt(live_url)  # 进一步获取 .txt 文件中的链接
        else:
            print(f"没有找到 'lives' 键或格式不正确: {url}")  # 打印没有 'lives' 键的 URL
    except requests.exceptions.RequestException as e:
        print(f"下载或解析 {url} 时发生错误: {e}")

# 保存有效的 URL 到 iptv.txt 文件（确保使用 UTF-8 编码）
with open("iptv.txt", "w", encoding="utf-8") as f:
    for url in valid_urls:
        f.write(url + "\n")

print(f"共有 {len(valid_urls)} 个有效的链接已保存到 iptv.txt")
