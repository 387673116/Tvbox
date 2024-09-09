import requests
import re

# 获取远程数据
url = 'https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 定义需要删除的 key 列表
    keys_to_remove = [
        "ConfigCenter",
        "csp_Kugou",
        "Aid",
        "蜡笔",
        "星剧社",
        "易搜",
        "csp_PanSearch",
        "纸条搜",
        "网盘集合",
        "Youtube",
        "TgYunPanLocal1",
        "TgYunPanLocal2",
        "TgYunPanLocal3",
        "TgYunPanLocal4",
        "TgYunPanLocal5",
        "push_agent",
        "csp_Local",
        "虎牙直播",
        "有声小说吧",
        "JRKAN直播",
        "88看球",
        "csp_Bili",
        "少儿",
        "小学",
        "初中",
        "高中"
    ]

    # 使用正则表达式删除包含这些 key 的部分
    for key in keys_to_remove:
        pattern = r'\{[^{}]*"key":"{}"[^{}]*\},?'.format(key, key)
        text = re.sub(pattern, '', text)

    # 保存结果到 index.json
    with open('index.json', 'w', encoding='utf-8') as f:
        f.write(text)

    print("index.json 文件已生成")

else:
    print("响应内容为空或状态码不是 200")
