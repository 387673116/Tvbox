import requests
import re

# 下载并读取 M3U 文件内容
def download_m3u(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"成功下载 M3U 文件: {url}")
        return response.text
    except requests.RequestException as e:
        print(f"无法下载 M3U 文件: {url}, 错误: {e}")
        return None

# 修改分类名称，支持修改现有分类和设置默认分类
def modify_category(m3u_data, category_map, default_category):
    lines = m3u_data.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            # 检查是否有现有分类
            match = re.search(r'tvg-name="([^"]*)"', line)
            if match:
                current_category = match.group(1)
                # 替换为指定的新分类
                if current_category in category_map:
                    line = line.replace(current_category, category_map[current_category])
            else:
                # 如果没有分类，添加默认分类
                line = line.rstrip() + f' tvg-name="{default_category}"'
        new_lines.append(line)
    return "\n".join(new_lines)

# 合并并保存 M3U 文件
def merge_m3u():
    # 下载两个 M3U 文件
    chinese_m3u = download_m3u("https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u")
    chinese_m3u = download_m3u("https://raw.githubusercontent.com/387673116/Tvbox/master/other/jingqu.m3u")
    international_m3u = download_m3u("https://aktv.top/live.m3u")
    
    if international_m3u and chinese_m3u:
        # 修改分类名称
        # 分类映射：将 AKTV 改为 "海外频道"
        category_map = {"AKTV": "海外频道"}
        # 默认分组：将无分组的频道改为 "央视频道"
        default_category = "央视频道"
        
        # 修改国际频道的分类
        international_m3u = modify_category(international_m3u, category_map, default_category)
        # 修改卫视频道的分类
        chinese_m3u = modify_category(chinese_m3u, category_map, default_category)

        # 合并两个 M3U 文件
        merged_m3u = international_m3u + "\n" + chinese_m3u

        # 保存到 iptv4.m3u 文件
        with open("iptv4.m3u", "w", encoding="utf-8") as f:
            f.write(merged_m3u)
        print("M3U 文件已成功合并并保存为 iptv4.m3u")
    else:
        print("未能成功下载所有 M3U 文件，合并失败")

if __name__ == "__main__":
    merge_m3u()
