import requests
import re
from collections import defaultdict

# IPTV源列表
urls = [
    "https://raw.githubusercontent.com/fanmingming/live/master/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/YanG-1989/m3u/master/Gather.m3u",
    "https://raw.githubusercontent.com/YueChan/live/master/APTV.m3u",
    "https://raw.githubusercontent.com/YueChan/live/master/Global.m3u",
    "https://raw.githubusercontent.com/387673116/Tvbox/master/other/jingqu.m3u",
    "https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt"
]

# 输出文件路径
output_file = "iptv6.txt"

# 需要删除的关键词列表
exclude_keywords = ["咪咕", "轮播", "解说", "炫舞", "埋堆堆", "斗鱼", "虎牙", "B站", "CETV", "叫啥"]

# 频道名称的替换规则 (注意包括逗号)
replace_rules = {
    "CCTV4美洲,": "CCTV-4 美洲,",
    "CCTV-4K,": "CCTV-4K 超高清,",
    "CCTV4欧洲,": "CCTV-4 欧洲,",
    "CCTV-1,": "CCTV-1 综合,",
    "CCTV-2,": "CCTV-2 财经,",
    "CCTV-3,": "CCTV-3 综艺,",
    "CCTV-4,": "CCTV-4 中文国际,",
    "CCTV-5,": "CCTV-5 体育,",
    "CCTV-5+,": "CCTV-5+ 体育赛事,",
    "CCTV-6,": "CCTV-6 电影,",
    "CCTV-7,": "CCTV-7 国防军事,",
    "CCTV-8,": "CCTV-8 电视剧,",
    "CCTV-9,": "CCTV-9 纪录,",
    "CCTV-10,": "CCTV-10 科教,",
    "CCTV-11,": "CCTV-11 戏曲,",
    "CCTV-12,": "CCTV-12 社会与法,",
    "CCTV-13,": "CCTV-13 新闻,",
    "CCTV-14,": "CCTV-14 少儿,",
    "CCTV-15,": "CCTV-15 音乐,",
    "CCTV-16,": "CCTV-16 奥林匹克,",
    "CCTV-17,": "CCTV-17 农业农村,"
}

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        print(f"成功获取内容，前500个字符如下:\n{response.text[:500]}")
        return response.text
    except requests.RequestException as e:
        print(f"请求 {url} 时出错: {e}")
        return None

def extract_group_title(line):
    """ 提取 group-title，兼容更多的 M3U 文件 """
    match = re.search(r'group-title\s*=\s*"([^"]+)"', line)
    if match:
        return match.group(1)
    return None

def clean_line(line):
    for keyword in exclude_keywords:
        if keyword in line:
            return None
    return line

def clean_group_title(category):
    """清理分类名称并进行分类合并"""
    category = category.replace("频道", "")
    if category in ["上海", "内蒙", "地方", "地区", "浙江"]:
        return "地区"
    if category == "4KIPV4":
        return "4K"
    return category

def apply_replace_rules(content):
    content_lines = content.splitlines()
    final_content = []
    for line in content_lines:
        for old, new in replace_rules.items():
            if old in line:
                line = line.replace(old, new)
        final_content.append(line)
    return "\n".join(final_content)

def format_and_merge_sources(urls, output_file):
    category_channels = defaultdict(list)
    for url in urls:
        print(f"正在处理: {url}")
        content = fetch_url_content(url)
        if content:
            lines = content.splitlines()
            category = None
            channel_name = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                cleaned_line = clean_line(line)
                if not cleaned_line:
                    continue
                if cleaned_line.startswith("#EXTINF"):
                    group_title = extract_group_title(cleaned_line)
                    if group_title:
                        category = clean_group_title(group_title.strip())
                        parts = cleaned_line.split(",")
                        if len(parts) > 1:
                            channel_name = parts[1].strip()
                elif cleaned_line.startswith("http"):
                    if category and channel_name:
                        if "叫啥" not in channel_name:  # 过滤掉名称包含“叫啥”的频道
                            category_channels[category].append((channel_name, cleaned_line))
                            channel_name = None
                elif ',' in cleaned_line and 'http' in cleaned_line:
                    # 兼容单行格式：频道名称,链接
                    parts = cleaned_line.split(',')
                    if len(parts) == 2:
                        channel_name, link = parts[0].strip(), parts[1].strip()
                        category = "未知分类"
                        if "叫啥" not in channel_name:
                            category_channels[category].append((channel_name, link))
    final_content = []
    for category, channels in category_channels.items():
        if "央视" in category:
            channels.sort(key=lambda x: x[0])  # 央视分类中对CCTV-1、CCTV-2等按顺序排序
        final_content.append(f"{category},#genre#")
        for channel_name, link in sorted(channels):
            final_content.append(f"{channel_name},{link}")
    final_output = apply_replace_rules("\n".join(final_content))
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(final_output)
    print(f"IPTV源内容已成功合并到 {output_file}")

if __name__ == "__main__":
    format_and_merge_sources(urls, output_file)
    print(f"IPTV源内容已成功合并到 {output_file}")
