import requests
import json
import re

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 删除以 // 开头的注释行
    cleaned_text = re.sub(r'^\s*//.*\n?', '', text, flags=re.MULTILINE)

    # 处理 JSON 数据
    try:
        data = json.loads(cleaned_text)

        # 删除指定 key 的项
        keys_to_remove = [
            'csp_Dm84', 'csp_Anime1', 'csp_Kugou', 'Aid', '易搜', 'csp_PanSearch', 
            '纸条搜', '网盘集合', '少儿', '初中', '高中', '小学', 'csp_Bili', '88看球', 
            '有声小说吧', '虎牙直播', 'csp_Local', 'push_agent', 'TgYunPanLocal5', 
            'TgYunPanLocal4', 'TgYunPanLocal3', 'TgYunPanLocal2', 'TgYunPanLocal1', 
            'Youtube'
        ]

        if 'sites' in data:
            # 打印所有 key 来进行调试
            print("处理前的所有 key：")
            for site in data['sites']:
                print(site.get('key'))

            # 执行删除操作
            data['sites'] = [site for site in data['sites'] if site.get('key') not in keys_to_remove]

            # 再次打印剩余的 key
            print("处理后的所有 key：")
            for site in data['sites']:
                print(site.get('key'))

            # 修改 "sites" 列表中 key 为 "csp_DouDou" 的项
            for site in data['sites']:
                if site.get('key') == 'csp_DouDou':
                    site['name'] = '🔍豆瓣TOP榜单'

        # 直接将 "lives" 列表中的 "url" 字段值替换为指定值
        if 'lives' in data:
            for live in data['lives']:
                if 'url' in live:
                    live['url'] = 'https://6851.kstore.space/zby.txt'

        # 保存结果到 index.json，并压缩为单行格式
        with open('index.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        print("压缩后的 index.json 文件已生成")

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")

else:
    print("响应内容为空或状态码不是 200")
