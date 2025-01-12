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
]

# 输出文件路径
output_file = "iptv6.txt"

# 需要删除的关键词列表
exclude_keywords = ["咪咕", "炫舞", "埋堆堆", "斗鱼", "虎牙", "B站", "CETV", "叫啥", "自贸", "英雄联盟音乐节", "漫游世界", "高清娱乐", "风尚音乐", "电子竞技", "百变课堂"]

# 频道名称的替换规则
replace_rules = {
    "CCTV1 综合,": "CCTV-1,",
    "CCTV2 财经,": "CCTV-2,",
    "CCTV3 综艺,": "CCTV-3,",
    "CCTV4 中文国际,": "CCTV-4,",
    "CCTV5 体育,": "CCTV5,",
    "CCTV5+ 体育赛事,": "CCTV-5+,",
    "CCTV6 电影,": "CCTV-6,",
    "CCTV7 国防军事,": "CCTV-7,",
    "CCTV8 电视剧,": "CCTV-8,",
    "CCTV9 纪录,": "CCTV-9,",
    "CCTV 10 科教,": "CCTV-10,",
    "CCTV 11 戏曲,": "CCTV-11,",
    "CCTV 12 社会与法,": "CCTV-12,",
    "CCTV 13 新闻,": "CCTV-13,",
    "CCTV 14 少儿,": "CCTV-14,",
    "CCTV 15 音乐,": "CCTV-15,",
    "CCTV 16 奥林匹克,": "CCTV-16,",
    "CCTV 17 农村农业,": "CCTV-17,", 
    "CCTV-4K,": "CCTV-4K,",
    "CCTV-4 欧洲,": "CCTV-4,",
    "CCTV-1 综合,": "CCTV-1,",
    "CCTV-2 财经,": "CCTV-2,",
    "CCTV-3 综艺,": "CCTV-3,",
    "CCTV-4 中文国际,": "CCTV-4,",
    "CCTV-5 体育,": "CCTV5,",
    "CCTV-5+ 体育赛事,": "CCTV-5+,",
    "CCTV-6 电影,": "CCTV-6,",
    "CCTV-7 国防军事,": "CCTV-7,",
    "CCTV-8 电视剧,": "CCTV-8,",
    "CCTV-9 纪录,": "CCTV-9,",
    "CCTV-10 科教,": "CCTV-10,",
    "CCTV-11 戏曲,": "CCTV-11,",
    "CCTV-12 社会与法,": "CCTV-12,",
    "CCTV-13 新闻,": "CCTV-13,",
    "CCTV-14 少儿,": "CCTV-14,",
    "CCTV-15 音乐,": "CCTV-15,",
    "CCTV-16 奥林匹克,": "CCTV-16,",
    "CCTV-17 农村农业,": "CCTV-17,", 
    "CCTV-17 农业农村,": "CCTV-17,", 
    "CCTV1,": "CCTV-1,",
    "CCTV2,": "CCTV-2,",
    "CCTV3,": "CCTV-3,",
    "CCTV4,": "CCTV-4,",
    "CCTV5,": "CCTV-5,",
    "CCTV5+,": "CCTV-5+,",
    "CCTV6,": "CCTV-6,",
    "CCTV7,": "CCTV-7,",
    "CCTV8,": "CCTV-8,",
    "CCTV9,": "CCTV-9,",
    "CCTV10,": "CCTV-10,",
    "CCTV11,": "CCTV-11,",
    "CCTV12,": "CCTV-12,",
    "CCTV13,": "CCTV-13,",
    "CCTV14,": "CCTV-14,",
    "CCTV15,": "CCTV-15,",
    "CCTV16,": "CCTV-16,",
    "CCTV17,": "CCTV-17,",
    "NewTV ": "",
    "SiTV ": "",
    "CHC 家庭影院,": "CHC家庭影院,",
    "CHC 动作电影,": "CHC动作电影,",
    "CHC 影迷电影,": "CHC影迷电影,",
    "CGTN 国际,": "CGTN国际,",
    "iHOT ": "",
    "iHOY ": ""
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
    return match.group(1) if match else None

def clean_line(line):
    """删除符号•、‘IPV6’关键字和‘「」’符号，并检查是否包含排除的关键词"""
    line = line.replace("•", "").replace("IPV6", "").replace("「", "").replace("」", "")
    for keyword in exclude_keywords:
        if keyword in line:
            return None  # 如果包含排除关键词，返回None表示该行应删除
    return line

def clean_group_title(category):
    """合并分类为地区，并去除‘频道’关键字"""
    # 删除“频道”关键字
    category = category.replace("频道", "")

    # 将 NewTV 分类改为数字
    if category == "NewTV":
        return "数字"

    # 合并分类为地区
    if category in ["地方", "地区", "内蒙", "浙江", "上海"]:
        return "地区"

    return category

def apply_replace_rules(content):
    """应用替换规则，修改频道名称"""
    for old, new in replace_rules.items():
        content = content.replace(old, new)
    return content

def extract_number_from_channel_name(channel_name):
    """从频道名称中提取数字，确保正确排序"""
    match = re.search(r'(\d+)', channel_name)
    return int(match.group(1)) if match else float('inf')  # 如果没有数字，放在最后

def format_and_merge_sources(urls, output_file):
    """将多个IPTV源内容合并为自定义txt格式"""
    category_channels = defaultdict(list)  # 使用defaultdict以便同名频道自动合并
    channel_name_count = defaultdict(int)  # 统计每个频道名称的出现次数

    for url in urls:
        print(f"正在处理: {url}")
        content = fetch_url_content(url)
        if content:
            lines = content.splitlines()
            category = None  # 当前的分类
            channel_name = None  # 当前频道名称
            for line in lines:
                line = line.strip()
                if not line:
                    continue  # 忽略空行

                cleaned_line = clean_line(line)
                if not cleaned_line:
                    continue  # 如果该行被删除，跳过

                if cleaned_line.startswith("#EXTINF"):
                    group_title = extract_group_title(cleaned_line)
                    if group_title:
                        category = clean_group_title(group_title.strip())
                        channel_name = cleaned_line.split(",")[1].strip()  # 获取频道名称
                elif cleaned_line.startswith("http"):
                    # 统计频道名称出现次数
                    channel_name_count[channel_name] += 1
                    if channel_name_count[channel_name] <= 6:
                        # 如果频道名称出现次数不超过6次，添加到分类中
                        category_channels[category].append((channel_name, cleaned_line))
                    else:
                        print(f"跳过频道: {channel_name}，已超过6次")

    # 删除4KIPV4和4K分类
    category_channels.pop("4KIPV4", None)
    category_channels.pop("4K", None)

    # 合并央视分类的CHC相关频道到数字分类
    chc_channels = []
    if "央视" in category_channels:
        category_channels["央视"] = [
            (channel_name, link) if not channel_name.startswith("CHC") else chc_channels.append((channel_name, link))
            for channel_name, link in category_channels["央视"]
        ]
        category_channels["央视"] = [item for item in category_channels["央视"] if item]  # 清理空值

    # 将CHC相关频道添加到数字分类
    if chc_channels:
        category_channels["数字"] = category_channels.get("数字", []) + chc_channels

    # 将"数字分类"改为"数字"
    if "数字分类" in category_channels:
        category_channels["数字"] = category_channels.pop("数字分类")

    # 格式化并输出
    with open(output_file, "w", encoding="utf-8") as outfile:
        final_content = []

        # 按顺序处理分类
        for key in ["央视", "卫视", "数字"]:
            if key in category_channels:
                final_content.append(f"{key},#genre#")
                channels = category_channels.pop(key)
                channels.sort(key=lambda x: extract_number_from_channel_name(x[0]))
                for channel_name, link in channels:
                    final_content.append(f"{channel_name},{link}")

        # 处理剩余的分类
        for category, channels in category_channels.items():
            if category == "温馨提示":
                continue  # 跳过温馨提示
            final_content.append(f"{category},#genre#")
            channels.sort(key=lambda x: extract_number_from_channel_name(x[0]))
            for channel_name, link in channels:
                final_content.append(f"{channel_name},{link}")

        # 应用替换规则并写入文件
        modified_content = apply_replace_rules("\n".join(final_content))
        outfile.write(modified_content)

if __name__ == "__main__":
    format_and_merge_sources(urls, output_file)
    print(f"IPTV源内容已成功合并到 {output_file}")
