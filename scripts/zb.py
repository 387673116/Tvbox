import requests
import re
import sys

def fetch_m3u_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.content
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        sys.exit(1)

def decode_content(content):
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return content.decode('gbk')
        except UnicodeDecodeError as e:
            print(f"解码错误: {e}")
            sys.exit(1)

def process_lines(lines):
    result = ["#EXTM3U"]
    current_category = None

    for line in lines:
        if "#genre#" in line:
            current_category = line.replace("#genre#", "").strip()
            continue
        
        if "," in line:
            channel_name, channel_url = line.split(",", 1)
            if current_category:
                current_category = re.sub(r'[，,]', '', current_category)
                result.append(f"#EXTINF:-1 group-title=\"{current_category}\", {channel_name.strip()}")
            else:
                result.append(f"#EXTINF:-1, {channel_name.strip()}")
            result.append(channel_url.strip())
    
    return result

def write_m3u_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as m3u_file:
            m3u_file.write("\n".join(content) + "\n")
    except IOError as e:
        print(f"文件写入错误: {e}")
        sys.exit(1)

def main():
    url = "https://6851.kstore.space/zby.txt"
    content = fetch_m3u_content(url)
    decoded_content = decode_content(content)
    lines = decoded_content.splitlines()
    result = process_lines(lines)
    write_m3u_file("zb.m3u", result)
    print("zb.m3u 任务已完成.")

if __name__ == "__main__":
    main()
