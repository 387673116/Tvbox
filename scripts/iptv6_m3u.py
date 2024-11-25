import requests
import re

# 需要处理的 M3U 文件 URLs
urls = [
    "https://raw.githubusercontent.com/fanmingming/live/master/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/YanG-1989/m3u/master/Gather.m3u",
    "https://raw.githubusercontent.com/YueChan/live/master/APTV.m3u",
    "https://raw.githubusercontent.com/YueChan/live/master/Global.m3u",
]

# 主模板文件（用于标准化属性）
template_url = urls[0]

# 下载文件
def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# 解析 M3U 文件
def parse_m3u(content):
    # 先将 tvg-id 替换为 tvg-name
    content = content.replace('tvg-id', 'tvg-name')
    
    # 正则表达式匹配 EXTINF 标签和播放链接
    pattern = re.compile(r'#EXTINF:-1(.*?),\s*(.+)\n(https?://.+)')
    entries = pattern.findall(content)
    parsed = []
    for match in entries:
        attributes, name, url = match
        attrs = dict(re.findall(r'(\w+?)="(.*?)"', attributes))
        attrs["tvg-name"] = name.strip()
        attrs["url"] = url.strip()
        parsed.append(attrs)
    return parsed

# 序列化 M3U 文件
def serialize_m3u(entries):
    lines = ["#EXTM3U"]
    for entry in entries:
        attributes = " ".join(f'{key}="{value}"' for key, value in entry.items() if key != "url" and key != "tvg-name")
        lines.append(f'#EXTINF:-1 {attributes},{entry["tvg-name"]}\n{entry["url"]}')
    return "\n".join(lines)

# 加载和合并所有 M3U 文件
def load_and_merge(urls, template_url):
    template_content = download_file(template_url)
    template_entries = parse_m3u(template_content)
    template_map = {entry["tvg-name"]: entry for entry in template_entries}

    merged_entries = []
    seen_names = {}

    for url in urls:
        content = download_file(url)
        entries = parse_m3u(content)

        for entry in entries:
            # 排除 group-title 包含 "咪咕" 的条目
            if "group-title" in entry and "咪咕" in entry["group-title"]:
                continue

            name = entry["tvg-name"]
            if name in template_map:
                # 统一属性（只更新除播放链接外的属性）
                template_entry = template_map[name]
                entry.update({
                    "name": template_entry.get("name", entry.get("name")),
                    "logo": template_entry.get("logo", entry.get("logo")),
                    "title": template_entry.get("title", entry.get("title")),
                })
            if name in seen_names:
                # 如果已经出现，确保一致性
                existing_entry = seen_names[name]
                for key in entry:
                    if key != "url" and key != "tvg-name":
                        entry[key] = existing_entry.get(key, entry[key])
            else:
                seen_names[name] = entry

            merged_entries.append(entry)

    return merged_entries

# 处理并生成最终的 M3U 文件
def main():
    merged_entries = load_and_merge(urls, template_url)
    output_content = serialize_m3u(merged_entries)
    with open("iptv6.m3u", "w", encoding="utf-8") as f:
        f.write(output_content)
    print("iptv6.m3u 文件已生成！")

if __name__ == "__main__":
    main()
