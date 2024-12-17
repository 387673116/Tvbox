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
        keys_to_remove = [
            'csp_Dm84', 'csp_Anime1', 'csp_Kugou', 'Aid', '易搜', 'csp_PanSearch', '短视频', 'TgYunPan|本地', 'csp_BookTing',
            '纸条搜', '网盘集合', '少儿', '初中', '高中', '小学', 'csp_Bili', '88看球', 'csp_Qiyou', 'csp_Alllive', 'csp_Kanqiu',
            '有声小说吧', '虎牙直播', 'csp_Local', 'push_agent', 'TgYunPanLocal5', 'csp_FengGo', '多多', 'MIUC', 'AList',
            'TgYunPanLocal4', 'TgYunPanLocal3', 'TgYunPanLocal2', 'TgYunPanLocal1', '酷奇MV', '斗鱼直播', '盘Ta',
            'Youtube', 'ConfigCenter', 'JRKAN直播', '星剧社', '蜡笔', '玩偶gg', 'csp_YGP', 'csp_SP360', '至臻'
        ]

        # 删除指定 key 的项，并去掉 name 中包含“墙外”或“木偶”的项
        if 'sites' in data:
            data['sites'] = [
                site for site in data['sites']
                if site.get('key') not in keys_to_remove and '墙外' not in site.get('name', '') and '木偶' not in site.get('name', '')
            ]

            # 修改指定 key 的 name 字段
            for site in data['sites']:
                if site.get('key') == 'csp_Douban':
                    site['name'] = '🔍豆瓣TOP榜'
                elif site.get('key') == 'csp_DouDou':
                    site['name'] = '🔍豆瓣TOP榜'
                elif site.get('key') == 'csp_Jianpian':
                    site['name'] = '⚡荐片'
                elif site.get('key') == 'csp_SixV':
                    site['name'] = '🌸新6V'

            # 将 "csp_Jianpian" 调整到第二个位置
            jianpian_site = next((site for site in data['sites'] if site.get('key') == 'csp_Jianpian'), None)
            if jianpian_site:
                data['sites'].remove(jianpian_site)
                data['sites'].insert(1, jianpian_site)

        # 替换 "lives" 列表中的数据
        # 保留 "lives" 列表中的第一组数据，并删除其他数据
        if 'lives' in data and len(data['lives']) > 0:
            # 删除除第一组外的所有数据
            data['lives'] = [data['lives'][0]]  # 只保留第一组数据

            # 替换第一组数据的 name 和 url
            data['lives'][0]['name'] = 'IPTV4'
            data['lives'][0]['url'] = 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv4.m3u'

            # 复制第一组数据，修改第二组和第三组的数据
            ipv6_data = {**data['lives'][0], 'name': 'IPTV6', 'url': 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv6.txt'}
            zonghe_data = {**data['lives'][0], 'name': '综合', 'url': 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/zonghe.m3u'}

            # 将修改后的数据添加到 "lives" 列表
            data['lives'].append(ipv6_data)
            data['lives'].append(zonghe_data)

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
