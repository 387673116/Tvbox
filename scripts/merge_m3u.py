import requests
import os
import hashlib

# 下载 M3U 文件
def download_m3u(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"无法下载 {url}: {e}")
        return ""

# 解析 M3U 文件
def parse_m3u(content):
    channels = []
    lines = content.strip().split("\n")
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            info = lines[i]
            url = lines[i + 1] if i + 1 < len(lines) else ""
            channels.append({"info": info, "url": url})
    return channels

# 合并频道列表
def merge_channels(*channel_lists):
    merged = []
    seen_urls = set()
    for channels in channel_lists:
        for channel in channels:
            if channel["url"] not in seen_urls:
                merged.append(channel)
                seen_urls.add(channel["url"])
    return merged

# 按分类排序
def sort_channels(channels):
    categories = {}
    for channel in channels:
        group = "未分类"
        match = re.search(r'group-title="([^"]+)"', channel["info"])
        if match:
            group = match.group(1)
        if group not in categories:
            categories[group] = []
        categories[group].append(channel)
    return categories

# 保存为 M3U 文件
def save_m3u(file_path, categories):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for category, channels in categories.items():
            f.write(f"\n# ---- {category} ----\n")
            for channel in channels:
                f.write(f"{channel['info']}\n{channel['url']}\n")

# 计算文件的哈希值
def calculate_hash(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# 主函数
def main():
    urls = [
        "https://iptv-org.github.io/iptv/index.m3u",
        "https://raw.githubusercontent.com/YueChan/Live/master/APTV.m3u",
        "https://raw.githubusercontent.com/YueChan/Live/master/Global.m3u",
    ]
    
    # 下载并解析 M3U 文件
    all_channels = []
    for url in urls:
        content = download_m3u(url)
        if content:
            all_channels.extend(parse_m3u(content))
    
    # 合并频道并分类
    merged_channels = merge_channels(all_channels)
    sorted_channels = sort_channels(merged_channels)
    
    # 临时保存优化后的文件
    temp_file = "optimized_channels.m3u"
    save_m3u(temp_file, sorted_channels)
    
    # 比较文件内容
    target_file = "iptv.m3u"
    temp_hash = calculate_hash(temp_file)
    target_hash = calculate_hash(target_file)
    
    if temp_hash == target_hash:
        print("文件未变化，不需要更新。")
        os.remove(temp_file)  # 删除临时文件
    else:
        print("文件已更新，替换现有文件。")
        os.replace(temp_file, target_file)

if __name__ == "__main__":
    main()
