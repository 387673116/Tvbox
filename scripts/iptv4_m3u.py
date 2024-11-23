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

# 修改分类名称（group-title），并处理没有 group-title 的情况
def modify_group_title(m3u_data, url, category_map):
    lines = m3u_data.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            # 检查是否存在 group-title
            match = re.search(r'group-title="([^"]*)"', line)
            if match:
                current_group = match.group(1)
                # 如果匹配到的 group-title 在分类映射中，则替换
                if current_group in category_map:
                    line = line.replace(f'group-title="{current_group}"', f'group-title="{category_map[current_group]}"')
            else:
                # 如果没有 group-title 且是指定的 URL，则添加默认分组
                if url == "https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u":
                    line = line.rstrip() + ' group-title="央视频道"'
        new_lines.append(line)
    return "\n".join(new_lines)

# 合并多个 M3U 文件内容
def merge_m3u_files(urls, output_file, category_map):
    merged_content = ""
    for url in urls:
        print(f"正在处理: {url}")
        m3u_data = download_m3u(url)
        if m3u_data:
            # 修改分类名称并合并
            m3u_data = modify_group_title(m3u_data, url, category_map)
            merged_content += m3u_data + "\n"
        else:
            print(f"跳过未成功下载的文件: {url}")
    
    if merged_content:
        # 保存合并后的内容到文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"M3U 文件已成功合并并保存为 {output_file}")
    else:
        print("未能合并任何有效的 M3U 数据。")

if __name__ == "__main__":
    # 定义所有要合并的 M3U 文件 URL
    m3u_urls = [
        "https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u",
        "https://raw.githubusercontent.com/387673116/Tvbox/master/other/jingqu.m3u",
        "https://aktv.top/live.m3u"
    ]
    
    # 分类映射：将指定分类名称替换为新的名称
    category_map = {
        "AKTV": "海外频道"
    }
    
    # 输出文件名
    output_file = "iptv4.m3u"
    
    # 开始合并
    merge_m3u_files(m3u_urls, output_file, category_map)
