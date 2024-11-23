import requests
import json

# 测试 URL 是否有效的函数
def is_valid_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# 从 URL 下载 JSON 数据并提取 'lives' 组的 URL 项
def extract_urls_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析 JSON 数据

        # 获取 'lives' 组中的 URL
        urls = []
        lives_group = data.get('lives', [])
        if lives_group:
            for entry in lives_group:
                url = entry.get('url')  # 获取每个 entry 的 URL
                if url:
                    urls.append((entry.get('group'), url))  # 存储分组和 URL
        return urls
    except requests.RequestException as e:
        print(f"无法从 {url} 获取数据: {e}")
        return []

# 过滤无效 URL 和 IPV6 URL
def filter_urls(urls):
    valid_urls = []
    for group, url in urls:
        if 'ipv6' in url.lower():
            continue  # 删除 IPV6 链接
        if is_valid_url(url):
            valid_urls.append((group, url))
    return valid_urls

# 生成新的 txt 文件
def generate_txt(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for group, url in urls:
            f.write(f"{group}, {url}\n")  # 每个分组和 URL 一行

# 主程序
def main():
    # JSON 文件的 URL 列表
    json_urls = [
        "https://notabug.org/qizhen15800/My9394/raw/master/%e4%b8%8d%e8%89%af%e5%b8%85.json",
        "https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json",
        "https://tv.lan2wan.top/candymuj.json",
        "http://home.jundie.top:81/top98.json"
    ]
    
    all_urls = []
    
    # 从每个 URL 下载并提取 URL
    for json_url in json_urls:
        print(f"正在处理 {json_url}...")
        urls = extract_urls_from_url(json_url)
        all_urls.extend(urls)
    
    # 过滤无效的 URL
    valid_urls = filter_urls(all_urls)
    
    # 生成新的 txt 文件
    output_file = 'iptv.txt'
    generate_txt(valid_urls, output_file)
    
    print(f"成功生成 TXT 文件：{output_file}")

# 执行脚本
if __name__ == '__main__':
    main()
