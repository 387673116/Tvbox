import requests
import json
import re

# 定义需要删除的关键词
keywords_to_remove = [
    "虎牙直播", "有声小说吧", "88看球", "少儿", "小学", "初中", 
    "墙外", "高中", "急救教学", "搜", "盘"
]

# 从指定链接获取 JSON 数据
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，则引发异常
    return response.json()

# 删除注释
def remove_comments(json_str):
    # 删除单行注释
    json_str = re.sub(r'//.*', '', json_str)
    # 删除多行注释
    json_str = re.sub(r'/\*[\s\S]*?\*/', '', json_str)
    return json_str

# 替换和删除指定的内容
def process_json(data):
    # 将 JSON 数据转化为字符串以便进行正则操作
    json_str = json.dumps(data, ensure_ascii=False)
    
    # 删除 JSON 字符串中的注释
    json_str = remove_comments(json_str)
    
    # 替换关键词
    json_str = json_str.replace("豆瓣┃本接口免费-🈲贩卖", "豆瓣TOP榜单")
    
    # 删除包含指定关键词的内容
    for keyword in keywords_to_remove:
        pattern = re.compile(r'\{[^{}]*' + re.escape(keyword) + r'[^{}]*\}(?:,)?')
        json_str = pattern.sub('', json_str)
    
    # 替换 live 项中的 URL（http 和 https）
    json_str = re.sub(r'("live"\s*:\s*")http[s]?://[^"]*(")', r'\1https://6851.kstore.space/zby.txt\2', json_str)

    # 清理多余的逗号和括号
    json_str = re.sub(r',\s*(?=\})', '', json_str)  # 删除}前的逗号
    json_str = re.sub(r'\{\s*}', '', json_str)  # 删除空的{}
    
    return json.loads(json_str)

# 主函数
def main():
    url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"
    json_data = fetch_json(url)
    processed_data = process_json(json_data)
    
    # 将处理后的数据输出为文件或其他形式
    with open('processed_data.json', 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
