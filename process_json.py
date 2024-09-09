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
    
    # 删除包含特定字符串的行
    lines = text.split('\n')
    lines = [line for line in lines if '//🐧裙：926953902' not in line]
    cleaned_text = '\n'.join(lines)

    # 替换特定 URL
    cleaned_text = cleaned_text.replace('https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt', 'https://6851.kstore.space/zby.txt')
    
    # 定义需要删除的关键字列表
    keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', '墙外', '高中', '急救教学', '搜', '盘']
    
    # 构建正则表达式，删除包含指定关键字的 {} 块及其后面的逗号
    for keyword in keywords:
        # 匹配形式为 {内容} 后面带一个逗号的形式
        pattern = r'\{[^{}]*' + re.escape(keyword) + r'[^{}]*\},?'
        cleaned_text = re.sub(pattern, '', cleaned_text)
    
    # 打印处理后的文本
    print("\n处理后的文本:")
    print(cleaned_text)
else:
    print("响应内容为空或状态码不是 200")
