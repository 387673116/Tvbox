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
            'csp_Dm84', 'csp_Anime1', 'csp_Kugou', 'Aid', '易搜', 'csp_PanSearch',  '短视频',
            '纸条搜', '少儿', '初中', '高中', '小学', 'csp_Bili', '88看球', 'csp_Qiyou',
            '有声小说吧', '虎牙直播', 'csp_Local', 'push_agent', 'TgYunPanLocal5', 'csp_FengGo',
            'TgYunPanLocal4', 'TgYunPanLocal3', 'TgYunPanLocal2', 'TgYunPanLocal1', '酷奇MV',
            'Youtube', 'JRKAN直播', '星剧社', '蜡笔', 'csp_YGP', 'csp_SP360'
        ]

        if 'sites' in data:
            # 保留不在 keys_to_remove 列表中的项
            data['sites'] = [site for site in data['sites'] if site.get('key') not in keys_to_remove]

            # 修改 "sites" 列表中 key 为 "csp_DouDou", "csp_Jianpian", "csp_SixV" 的项
            for site in data['sites']:
                if site.get('key') == 'csp_DouDou':
                    site['name'] = '🔍豆瓣TOP榜'
                elif site.get('key') == 'csp_Jianpian':
                    site['name'] = '⚡荐片'
                elif site.get('key') == 'csp_SixV':
                    site['name'] = '🌸新6V'

            # 将 "ConfigCenter" 移动到 "玩偶gg" 后面
            config_center_site = next((site for site in data['sites'] if site.get('key') == 'ConfigCenter'), None)
            wanou_gg_site = next((site for site in data['sites'] if site.get('key') == '玩偶gg'), None)
            if config_center_site and wanou_gg_site:
                data['sites'].remove(config_center_site)
                wanou_gg_index = data['sites'].index(wanou_gg_site)
                data['sites'].insert(wanou_gg_index + 1, config_center_site)

            # 修改 "玩偶gg" 的 name
            for site in data['sites']:
                if site.get('key') == '玩偶gg':
                    site['name'] = '⚽玩偶网盘'

            # 调整 "csp_Jianpian" 到第二个位置
            jianpian_site = next((site for site in data['sites'] if site.get('key') == 'csp_Jianpian'), None)
            if jianpian_site:
                data['sites'].remove(jianpian_site)
                data['sites'].insert(1, jianpian_site)

        # 直接将 "lives" 列表中的 "url" 字段值替换为指定值
        if 'lives' in data:
            for live in data['lives']:
                if 'url' in live:
                    live['url'] = 'https://6851.kstore.space/zby.txt'
                    
        # 保存处理后的数据为压缩的 JSON 格式
        with open('index.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

        print("压缩后的 index.json 文件已生成")

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")

else:
    print("响应内容为空或状态码不是 200")
