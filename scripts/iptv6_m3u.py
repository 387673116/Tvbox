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

# 过滤并去除指定的关键字和符号，同时保留其他符号
def remove_keywords_and_special_chars(m3u_content):
    lines = m3u_content.splitlines()
    filtered_lines = []
    remove_keywords = ["咪咕", "虎牙", "斗鱼", "埋堆", "轮播", "上海", "内蒙", "B站", "IPV6"]

    skip_next_line = False  # 用来标记是否跳过播放链接行

    for line in lines:
        if line.startswith("#EXTINF:"):
            # 检查频道名称是否包含要删除的关键词
            if any(keyword in line for keyword in remove_keywords):
                skip_next_line = True  # 如果包含这些关键词，则跳过下一行（播放链接）
                continue  # 跳过当前频道的描述行
            
            # 删除“频道”和“IPV6”关键字，但保留其他内容
            line = re.sub(r"频道", "", line)
            line = re.sub(r"IPV6", "", line)

            # 去除中文引号「」和符号“•”
            line = re.sub(r"[「」•]", "", line)

        if skip_next_line:
            skip_next_line = False  # 跳过播放链接行
            continue
        
        filtered_lines.append(line)
    
    return "\n".join(filtered_lines)

# 合并多个 M3U 文件并去除指定关键字和符号
def merge_m3u(urls):
    merged_content = "#EXTM3U\n"  # M3U 文件的开头
    for url in urls:
        print(f"正在处理: {url}")
        m3u_content = download_m3u(url)
        if m3u_content:
            filtered_content = remove_keywords_and_special_chars(m3u_content)
            merged_content += filtered_content + "\n"
    return merged_content

# 主函数
def main():
    urls = [
        "https://gh.999986.xyz/https://raw.githubusercontent.com/fanmingming/live/master/tv/m3u/ipv6.m3u",
        "https://gh.999986.xyz/https://raw.githubusercontent.com/YanG-1989/m3u/master/Gather.m3u",
        "https://gh.999986.xyz/https://raw.githubusercontent.com/YueChan/live/master/APTV.m3u",
        "https://gh.999986.xyz/https://raw.githubusercontent.com/YueChan/live/master/Global.m3u"
    ]

    # 合并并过滤内容
    merged_m3u = merge_m3u(urls)

    # 保存为 iptv6.m3u 文件
    with open("iptv6.m3u", "w") as f:
        f.write(merged_m3u)

    print("iptv6.m3u 文件已生成！")

if __name__ == "__main__":
    main()
