import requests
import json

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 删除注释行
    text = re.sub(r'^\s*//.*$', '', text, flags=re.MULTILINE)

    # 解析 JSON 数据
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        exit()

    # 定义需要删除的关键词
    keywords_to_remove = [
        "网盘", "本地", "高中", "初中", "小学", "少儿", "哔哩哔哩", "看球", "有声小说",
        "虎牙直播", "推送", "墙外", "搜", "急救教学", "动漫"
    ]

    # 删除包含特定关键词的条目
    filtered_sites = []
    for site in data.get('sites', []):
        should_remove = False
        for keyword in keywords_to_remove:
            if keyword in site.get('name', '') or keyword in site.get('key', ''):
                should_remove = True
                break
        if not should_remove:
            filtered_sites.append(site)

    # 更新 JSON 数据
    data['sites'] = filtered_sites

    # 保存结果到 index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("index.json 文件已生成")

else:
    print("响应内容为空或状态码不是 200")
