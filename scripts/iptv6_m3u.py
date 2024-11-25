import requests
import re
from collections import defaultdict

# 下载并解析 M3U 文件的函数
def download_m3u(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应失败，抛出异常
        return response.text
    except requests.RequestException as e:
        print(f"下载文件失败: {url}, 错误: {e}")
        return None

# 过滤并去除指定的关键字和符号，同时保留其他符号
def remove_keywords_and_special_chars(m3u_content):
    lines = m3u_content.splitlines()
    filtered_lines = []
    remove_keywords = ["咪咕", "虎牙", "斗鱼", "埋堆", "轮播", "上海", "内蒙", "B站", "IPV6", "地方", "炫舞未来"]

    skip_next_line = False  # 用来标记是否跳过播放链接行
    first_extm3u = True  # 用来标记是否已添加过 #EXTM3U 标签
    first_x_tvg_url = True  # 用来标记是否已添加过 x-tvg-url 标签

    channel_links = defaultdict(list)  # 用来存储相同频道名称的多个播放链接
    current_extinf_line = None  # 用来存储当前的 #EXTINF: 描述行

    for line in lines:
        # 跳过空白行
        if not line.strip():
            continue

        if line.startswith("#EXTM3U"):
            # 只保留第一个 #EXTM3U 标签
            if first_extm3u:
                filtered_lines.append(line)
                first_extm3u = False
            continue  # 跳过后续的 #EXTM3U 标签
        
        if line.startswith("x-tvg-url"):
            # 只保留第一个 x-tvg-url 标签
            if first_x_tvg_url:
                filtered_lines.append(line)
                first_x_tvg_url = False
            continue  # 跳过后续的 x-tvg-url 标签

        if line.startswith("#EXTINF:"):
            # 检查频道名称是否包含要删除的关键词
            if any(keyword in line for keyword in remove_keywords):
                skip_next_line = True  # 如果包含这些关键词，则跳过下一行（播放链接）
                continue  # 跳过当前频道的描述行

            # 删除“频道”和“IPV6”关键字，但保留其他内容
            line = re.sub(r"频道", "", line)
            line = re.sub(r"IPV6", "", line)
            line = re.sub(r" 综合", "", line)
            line = re.sub(r" 财经", "", line)
            line = re.sub(r" 综艺", "", line)
            line = re.sub(r" 科教", "", line)
            line = re.sub(r" 中文国际", "", line)
            line = re.sub(r" 体育赛事", "", line)
            line = re.sub(r" 体育", "", line)
            line = re.sub(r" 戏曲", "", line)
            line = re.sub(r" 电影", "", line)
            line = re.sub(r" 国防军事", "", line)
            line = re.sub(r" 电视剧", "", line)
            line = re.sub(r" 纪录", "", line)
            line = re.sub(r" 社会与法", "", line)
            line = re.sub(r" 新闻", "", line)
            line = re.sub(r" 少儿", "", line)
            line = re.sub(r" 音乐", "", line)
            line = re.sub(r" 奥林匹克", "", line)
            line = re.sub(r" 农业农村", "", line)
            line = re.sub(r"CCTV4欧洲", "CCTV-4 欧洲", line)
            line = re.sub(r"CCTV4美洲", "CCTV-4 美洲", line)
            line = re.sub(r"tvg-id", "tvg-name", line)

            # 去除中文引号「」和符号“•”
            line = re.sub(r"[「」•]", "", line)

            # 保存当前的 #EXTINF: 描述行
            current_extinf_line = line

        if skip_next_line:
            skip_next_line = False  # 跳过播放链接行
            continue
        
        # 存储每个频道的播放链接
        if current_extinf_line and not line.startswith("#EXTINF:"):
            # 关联当前频道的描述行与播放链接
            channel_name = re.search(r",([^,]+)$", current_extinf_line)  # 提取频道名称
            if channel_name:
                channel_name = channel_name.group(1).strip()
                channel_links[channel_name].append(current_extinf_line)  # 添加描述行
                channel_links[channel_name].append(line)  # 添加播放链接

            # 清空当前的描述行
            current_extinf_line = None

    # 合并每个频道的描述行和播放链接
    final_lines = []
    for channel_name, lines in channel_links.items():
        for i in range(0, len(lines), 2):  # 每两个元素一组，第一项为描述，第二项为播放链接
            final_lines.append(lines[i])  # 描述行
            final_lines.append(lines[i + 1])  # 播放链接

    return "\n".join(final_lines)

# 合并多个 M3U 文件并去除指定关键字和符号
def merge_m3u(urls):
    merged_content = ""
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
