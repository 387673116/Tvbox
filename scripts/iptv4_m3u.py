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

# 修改分类名称（group-title），并设置默认分组
def modify_group_title(m3u_data, category_map, default_group):
    lines = m3u_data.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            # 检查是否存在 group-title
            match = re.search(r'group-title="([^"]*)"', line)
            if match:
                current_group = match.group(1)
                # 替换分类名称
                if current_group in category_map:
                    line = line.replace(f'group-title="{current_group}"', f'group-title="{category_map[current_group]}"')
            else:
                # 如果没有 group-title，添加默认分组
                line = line.rstrip() + f' group-title="{default_group}"'
        new_lines.append(line)
    return "\n".join(new_lines)

# 合并并保存 M3U 文件
def merge_m3u():
    # 下载两个 M3U 文件
    chinese_m3u = download_m3u("https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u")
    international_m3u = download_m3u("https://aktv.top/live.m3u")
    
    if international_m3u and chinese_m3u:
        # 分类映射：将 AKTV 改为 "海外频道"
        category_map = {"AKTV": "海外频道"}
        # 默认分组：无 group-title 时设置为 "央视频道"
        default_group = "央视频道"
        
        # 修改国际频道的分类
        international_m3u = modify_group_title(international_m3u, category_map, default_group)
        # 修改卫视频道的分类
        chinese_m3u = modify_group_title(chinese_m3u, category_map, default_group)

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
