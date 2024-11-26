import requests

# IPTV源列表
urls = [
    "https://gh.999986.xyz/https://raw.githubusercontent.com/fanmingming/live/master/tv/m3u/ipv6.m3u",
    "https://gh.999986.xyz/https://raw.githubusercontent.com/YanG-1989/m3u/master/Gather.m3u",
    "https://gh.999986.xyz/https://raw.githubusercontent.com/YueChan/live/master/APTV.m3u",
    "https://gh.999986.xyz/https://raw.githubusercontent.com/YueChan/live/master/Global.m3u",
    "https://raw.githubusercontent.com/387673116/Tvbox/master/other/jingqu.m3u",
    "https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt"
]

# 输出文件路径
output_file = "iptv6.txt"

def fetch_url_content(url):
    """从指定URL获取内容"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

def merge_sources(urls, output_file):
    """将多个IPTV源内容合并为一个文件"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for url in urls:
            print(f"正在处理: {url}")
            content = fetch_url_content(url)
            if content:
                outfile.write(content + "\n\n")  # 写入文件，每个源之间用空行分隔
            else:
                print(f"跳过: {url}")

if __name__ == "__main__":
    merge_sources(urls, output_file)
    print(f"IPTV源内容已成功合并到 {output_file}")
