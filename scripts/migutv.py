import requests
import re
import os

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def fetch_m3u_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        try:
            return response.content.decode('utf-8')
        except UnicodeDecodeError:
            return response.content.decode('gbk')
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        exit(1)

def process_m3u_content(content):
    lines = content.splitlines()
    start_keyword = "咪咕移动,#genre#"
    capture = False
    result = ["#EXTM3U"]

    for line in lines:
        if start_keyword in line:
            capture = True
            continue

        if capture:
            if line.strip() == "":
                break

            if "," in line:
                channel_name, channel_url = line.split(",", 1)
                channel_url = channel_url.strip()
                if is_valid_url(channel_url):
                    result.append(f"#EXTINF:-1 group-title=\"咪咕视频\", {channel_name.strip()}")
                    result.append(channel_url)

    return result

def write_m3u_file(filename, content):
    try:
        # 获取当前工作目录，确保文件写入根目录
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w", encoding="utf-8") as m3u_file:
            for line in content:
                if line != "#EXTINF:-1 group-title=\"咪咕视频\", 咪咕视频":
                    m3u_file.write(line + "\n")
        print(f"{filepath} 任务已完成.")
    except IOError as e:
        print(f"文件操作错误: {e}")
        exit(1)

def main():
    url = "https://6851.kstore.space/zby.txt"
    content = fetch_m3u_file(url)
    processed_content = process_m3u_content(content)
    # 保存到仓库根目录
    write_m3u_file("migutv.m3u", processed_content)

if __name__ == "__main__":
    main()
