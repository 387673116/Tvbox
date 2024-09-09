import requests
import json

# 目标 URL
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'

# 发起请求获取 JSON 数据
response = requests.get(url)
data = response.json()

# 需要删除的键
keys_to_remove = [
    "csp_Dm84", "csp_Anime1", "csp_Kugou", "Aid", "易搜", "csp_PanSearch", "纸条搜",
    "网盘集合", "少儿", "初中", "高中", "小学", "csp_Bili", "88看球", "有声小说吧",
    "虎牙直播", "csp_Local", "push_agent", "TgYunPanLocal5", "TgYunPanLocal4",
    "TgYunPanLocal3", "TgYunPanLocal2", "TgYunPanLocal1", "Youtube"
]

# 处理数据
new_sites = []
for site in data.get('sites', []):
    if site.get('key') not in keys_to_remove:
        # 替换字符串
        if site.get('name') == "🔍豆瓣┃本接口免费-🈲贩卖":
            site['name'] = "豆瓣TOP榜单"
        
        # 替换 URL
        if isinstance(site.get('ext'), dict):
            filter_url = site['ext'].get('filter')
            if filter_url and filter_url.startswith('https://github.moeyy.xyz/'):
                site['ext']['filter'] = filter_url.replace('https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/sub/wogg.json', 'https://6851.kstore.space/zby.txt')
        elif isinstance(site.get('ext'), str):
            site['ext'] = site['ext'].replace('https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/sub/wogg.json', 'https://6851.kstore.space/zby.txt')

        # 添加到新列表
        new_sites.append(site)

# 保存修改后的数据
with open('index.json', 'w', encoding='utf-8') as f:
    json.dump({'sites': new_sites}, f, ensure_ascii=False, indent=4)
