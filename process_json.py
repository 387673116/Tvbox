import requests
import re

# 获取远程数据
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")

if response.status_code == 200 and response.text.strip():
    # 获取响应文本
    text = response.text

    # 提取 "sites":[ 到 "lives":[ 之间的内容
    match = re.search(r'"sites":\[(.*?)\]"lives":\[{', text, re.DOTALL)
    if match:
        sites_content = match.group(1)
        
        # 检查并删除包含关键字的部分
        keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', '墙外', '高中', '急救教学', '搜', '盘']
        
        # 定义正则表达式以匹配包含关键字的部分
        def delete_keywords(content):
            for keyword in keywords:
                # 匹配包含关键字的部分，并删除到关键字前后的大括号
                content = re.sub(r'\{[^{}]*' + re.escape(keyword) + r'[^{}]*\}', '', content)
            return content
        
        cleaned_sites_content = delete_keywords(sites_content)
        
        # 重新构造文本
        updated_text = text.replace(sites_content, cleaned_sites_content)
        
        # 打印替换后的文本
        print("\n处理后的文本:")
        print(updated_text)
    else:
        print("无法找到指定的内容范围")
else:
    print("响应内容为空或状态码不是 200")
