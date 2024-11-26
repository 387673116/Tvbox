import requests
import re
from collections import defaultdict

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

# 需要删除的关键词列表
exclude_keywords = ["咪咕", "轮播", "解说", "炫舞", "埋堆堆", "斗鱼", "虎牙", "B站", "CETV"]

# 频道名称的替换规则 (注意包括逗号)
replace_rules = {
    "CCTV4美洲,": "CCTV-4 美洲,",
    "CCTV-4K,": "CCTV-4K 超高清,",
    "CCTV4欧洲,": "CCTV-4 欧洲,",
    "CCTV1 综合,": "CCTV-1 综合,",
    "CCTV2 财经,": "CCTV-2 财经,",
    "CCTV3 综艺,": "CCTV-3 综艺,",
    "CCTV4 中文国际,": "CCTV-4 中文国际,",
    "CCTV5 体育,": "CCTV-5 体育,",
    "CCTV5+ 体育赛事,": "CCTV-5+ 体育赛事,",
    "CCTV6 电影,": "CCTV-6 电影,",
    "CCTV7 国防军事,": "CCTV-7 国防军事,",
    "CCTV8 电视剧,": "CCTV-8 电视剧,",
    "CCTV9 纪录,": "CCTV-9 纪录,",
    "CCTV 10 科教,": "CCTV-10 科教,",
    "CCTV 11 戏曲,": "CCTV-11 戏曲,",
    "CCTV 12 社会与法,": "CCTV-12 社会与法,",
    "CCTV 13 新闻,": "CCTV-13 新闻,",
    "CCTV 14 少儿,": "CCTV-14 少儿,",
    "CCTV 15 音乐,": "CCTV-15 音乐,",
    "CCTV 16 奥林匹克,": "CCTV-16 奥林匹克,",
    "CCTV 17 农村农业,": "CCTV-17 农业农村,",
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
    """从指定URL获取内容"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

def extract_group_title(line):
    """从EXTINF行提取group-title的值"""
    match = re.search(r'group-title="([^"]+)"', line)
    if match:
        return match.group(1)
    return None

def clean_line(line):
    """删除符号•、‘IPV6’关键字和‘「」’符号，并检查是否包含排除的关键词"""
    # 删除符号•、‘IPV6’关键字和‘「」’符号
    line = line.replace("•", "").replace("IPV6", "").replace("「", "").replace("」", "")
    
    # 检查是否包含需要排除的关键词
    for keyword in exclude_keywords:
        if keyword in line:
            return None  # 如果包含排除关键词，返回None表示该行应删除
    
    return line

def clean_group_title(category):
    """如果分类包含 '频道'，删除 '频道' 两个字"""
    return category.replace("频道", "") if "频道" in category else category

def apply_replace_rules(content):
    """应用替换规则，修改央视分类下的频道名称"""
    content_lines = content.splitlines()
    final_content = []
    for line in content_lines:
        # 替换频道名称（含逗号）
        for old, new in replace_rules.items():
            if old in line:
                line = line.replace(old, new)
        final_content.append(line)
    
    return "\n".join(final_content)

def extract_number_from_channel_name(channel_name):
    """从频道名称中提取数字，确保正确排序"""
    match = re.search(r'(\d+)', channel_name)
    if match:
        return int(match.group(1))
    return float('inf')  # 如果没有数字，放在最后

def format_and_merge_sources(urls, output_file):
    """将多个IPTV源内容合并为自定义txt格式"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        category_channels = defaultdict(list)  # 使用defaultdict以便同名频道自动合并

        for url in urls:
            print(f"正在处理: {url}")
            content = fetch_url_content(url)
            if content:
                # 按行处理内容
                lines = content.splitlines()
                category = None  # 当前的分类
                channel_name = None  # 当前频道名称
                for line in lines:
                    line = line.strip()
                    if not line:  # 忽略空行
                        continue
                    
                    # 清理行中的符号和关键词
                    cleaned_line = clean_line(line)
                    if not cleaned_line:  # 如果该行被删除，跳过
                        continue
                    
                    # 查找频道的相关信息
                    if cleaned_line.startswith("#EXTINF"):
                        # 解析EXTINF，提取分类和频道信息
                        group_title = extract_group_title(cleaned_line)
                        if group_title:
                            category = group_title.strip()  # 提取并格式化分类
                            category = clean_group_title(category)  # 删除"频道"字样
                            parts = cleaned_line.split(",")
                            channel_name = parts[1].strip()  # 获取频道名称
                    elif cleaned_line.startswith("http"):  # 播放链接
                        # 将播放链接和频道名称添加到分类对应的列表中
                        category_channels[category].append((channel_name, cleaned_line))

        # 将格式化后的分类和频道输出到文件
        final_content = []
        for category, channels in category_channels.items():
            # 输出group-title和#genre#（只保留分类名）
            formatted_category = category  # 直接使用category，已经是干净的名称
            final_content.append(f"{formatted_category},#genre#")
            # 对每个分类下的频道按名称中提取的数字进行排序
            channels.sort(key=lambda x: extract_number_from_channel_name(x[0]))  # 根据频道名称中的数字部分排序
            for channel_name, link in channels:
                final_content.append(f"{channel_name},{link}")
        
        # 应用替换规则并写入文件
        modified_content = apply_replace_rules("\n".join(final_content))
        outfile.write(modified_content)

if __name__ == "__main__":
    format_and_merge_sources(urls, output_file)
    print(f"IPTV源内容已成功合并到 {output_file}")
