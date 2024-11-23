import requests
import json
import re
import hashlib


def fetch_remote_data(url):
    try:
        response = requests.get(url)
        print(f"响应状态码: {response.status_code}")
        if response.status_code == 200 and response.text.strip():
            return response.text
        else:
            print("响应内容为空或状态码不是 200")
            return None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def clean_text(text):
    # 删除以 // 开头的注释行
    text = re.sub(r'^\s*//.*\n?', '', text, flags=re.MULTILINE)

    # 匹配以 http 或 https 开头的链接并替换域名
    domain_pattern = r'https?://[^/]+/(https?://[\w./-]+)'
    return re.sub(domain_pattern, r'https://gh.999986.xyz/\1', text)


def process_json_data(cleaned_text):
    try:
        data = json.loads(cleaned_text)

        # 修改 "lives" 列表中的数据
        if 'lives' in data:
            # 创建 IPV4 组
            ipv4_group = {
                'name': 'IPV4',
                'url': 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv4.m3u'
            }

            # 创建 IPV6 组
            ipv6_group = {
                'name': 'IPV6',
                'url': 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv6.m3u'
            }

            # 只保留 IPV4 和 IPV6 两组
            data['lives'] = [ipv4_group, ipv6_group]

        return data

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None


def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        print(f"压缩后的 {filename} 文件已生成")
    except IOError as e:
        print(f"文件保存错误: {e}")


def compare_json_files(existing_file, new_data):
    try:
        # 如果文件存在，则读取并对比
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

        # 比较两者的内容是否相同
        existing_hash = hashlib.md5(json.dumps(existing_data, ensure_ascii=False).encode('utf-8')).hexdigest()
        new_hash = hashlib.md5(json.dumps(new_data, ensure_ascii=False).encode('utf-8')).hexdigest()

        return existing_hash != new_hash  # 如果内容不同，返回 True

    except FileNotFoundError:
        return True  # 如果文件不存在，认为内容不同，需要更新
    except Exception as e:
        print(f"文件对比时发生错误: {e}")
        return False


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
    raw_text = fetch_remote_data(url)

    if raw_text:
        cleaned_text = clean_text(raw_text)
        processed_data = process_json_data(cleaned_text)

        if processed_data:
            # 检查当前目录的 index.json 是否需要更新
            if compare_json_files('index.json', processed_data):
                save_to_json(processed_data, 'index.json')
            else:
                print("index.json 内容未变化，未进行更新。")
