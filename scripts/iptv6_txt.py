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

def format_category(category):
    """如果分类包含 '频道'，删除 '频道' 两个字"""
    return category.replace("频道", "") if "频道" in category else category

def format_and_merge_sources(urls, output_file):
    """将多个IPTV源内容合并为自定义txt格式"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for url in urls:
            print(f"正在处理: {url}")
            content = fetch_url_content(url)
            if content:
                # 按行处理内容
                lines = content.splitlines()
                
                for line in lines:
                    line = line.strip()
                    if not line:  # 忽略空行
                        continue
                    
                    # 查找频道的相关信息
                    if line.startswith("#EXTINF"):
                        # 解析EXTINF，提取分类和频道信息
                        parts = line.split(",")
                        if len(parts) >= 2:
                            category = parts[0].replace("#EXTINF:-1,", "").strip()  # 获取分类
                            channel_name = parts[1].strip()  # 获取频道名称
                    elif line.startswith("http"):  # 播放链接
                        # 格式化分类，如果分类包含“频道”则删除“频道”
                        formatted_category = format_category(category)
                        # 输出符合格式的内容
                        outfile.write(f"{formatted_category},#genre#\n{channel_name},{line}\n")
            else:
                print(f"跳过: {url}")

if __name__ == "__main__":
    format_and_merge_sources(urls, output_file)
    print(f"IPTV源内容已成功合并到 {output_file}")
