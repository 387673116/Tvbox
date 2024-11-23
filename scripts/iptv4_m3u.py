import requests

# 下载并读取 M3U 文件内容
def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download M3U from {url}")
        return None

# 修改分类名称
def modify_category(m3u_data, old_category, new_category):
    lines = m3u_data.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#EXTINF:") and old_category in line:
            line = line.replace(old_category, new_category)
        new_lines.append(line)
    return "\n".join(new_lines)

# 合并并保存 M3U 文件
def merge_m3u():
    # 下载两个 M3U 文件
    international_m3u = download_m3u("https://aktv.top/live.m3u")
    chinese_m3u = download_m3u("https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u")

    if international_m3u and chinese_m3u:
        # 修改分类名称
        international_m3u = modify_category(international_m3u, "分类名称", "国际")
        chinese_m3u = modify_category(chinese_m3u, "分类名称", "卫视")

        # 合并两个 M3U 文件
        merged_m3u = international_m3u + "\n" + chinese_m3u

        # 保存到 ipv4.m3u 文件
        with open("ipv4.m3u", "w", encoding="utf-8") as f:
            f.write(merged_m3u)
        print("M3U 文件已成功合并并保存为 ipv4.m3u")
    else:
        print("未能成功下载所有 M3U 文件，合并失败")

if __name__ == "__main__":
    merge_m3u()
