import requests
import re

def fetch_m3u_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            content = response.content.decode('gbk')
        return content
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        exit(1)

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def process_m3u_content(content):
    lines = content.splitlines()
    start_keyword = "咪咕移动,#genre#"
    capture = False
    result = ["#EXTM3U"]
    category_name = "咪咕视频"

    # 遍历文件的每一行
    for line in lines:
        if start_keyword in line:
            capture = True
            # 添加分类信息行
            result.append(f"#EXTINF:-1 group-title=\"{category_name}\", {category_name}")
            continue

        if capture:
            if line.strip() == "":
                break
            if "," in line:
                channel_name, channel_url = line.split(",", 1)
                channel_url = channel_url.strip()
                if is_valid_url(channel_url):
                    result.append(f"#EXTINF:-1 group-title=\"{category_name}\", {channel_name.strip()}")
                    result.append(channel_url)

    return result

def write_m3u_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as m3u_file:
            m3u_file.write("\n".join(content))
        print(f"{filename} 任务已完成.")
    except IOError as e:
        print(f"文件操作错误: {e}")
        exit(1)

def main():
    url = "https://6851.kstore.space/zby.txt"
    content = fetch_m3u_file(url)
    processed_content = process_m3u_content(content)
    write_m3u_file("migutv.m3u", processed_content)

if __name__ == "__main__":
    main()
