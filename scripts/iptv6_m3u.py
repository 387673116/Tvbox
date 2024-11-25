import requests
import re

# 下载并解析 M3U 文件的函数
def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"无法下载文件: {url}")
        return None

# 过滤包含 "IPV6" 关键字的频道
def filter_channels(m3u_content):
    lines = m3u_content.splitlines()
    filtered_lines = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            if "IPV6" not in line:
                filtered_lines.append(line)
        else:
            if not line.startswith("#") and "IPV6" not in line:
                filtered_lines.append(line)
    return "\n".join(filtered_lines)

# 合并多个 M3U 文件并去除包含 "IPV6" 的频道
def merge_m3u(urls):
    merged_content = "#EXTM3U\n"  # M3U 文件的开头
    for url in urls:
        print(f"正在处理: {url}")
        m3u_content = download_m3u(url)
        if m3u_content:
            filtered_content = filter_channels(m3u_content)
            merged_content += filtered_content + "\n"
    return merged_content

# 主函数
def main():
    urls = [
        "https://raw.githubusercontent.com/fanmingming/live/master/tv/m3u/ipv6.m3u",
        "https://raw.githubusercontent.com/YanG-1989/m3u/master/Gather.m3u",
        "https://raw.githubusercontent.com/YueChan/live/master/APTV.m3u",
        "https://raw.githubusercontent.com/YueChan/live/master/Global.m3u"
    ]

    # 合并并过滤内容
    merged_m3u = merge_m3u(urls)

    # 保存为 iptv6.m3u 文件
    with open("iptv6.m3u", "w") as f:
        f.write(merged_m3u)

    print("iptv6.m3u 文件已生成！")

if __name__ == "__main__":
    main()
