import requests
import json
import socket
from urllib.parse import urlparse

# 定义要检查的 URL 列表
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
            return False
    except requests.exceptions.RequestException:
        return False

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
    except requests.exceptions.RequestException as e:
        print(f"下载或解析 {url} 时发生错误: {e}")

# 保存有效的 URL 到 iptv.txt 文件
with open("iptv.txt", "w", encoding="utf-8") as f:
    for url in valid_urls:
        f.write(url + "\n")

print(f"共有 {len(valid_urls)} 个有效的链接已保存到 iptv.txt")
