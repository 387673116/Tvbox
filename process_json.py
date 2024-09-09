import requests
import json

# 获取远程数据
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")
print("响应内容:")
print(response.text)

# 检查响应是否成功且内容是否为空
if response.status_code == 200 and response.text.strip():
    # 尝试解析 JSON 数据
    try:
        data = response.json()

        # 删除包含特定字符串的行
        json_str = json.dumps(data, ensure_ascii=False)
        lines = json_str.split('\n')
        lines = [line for line in lines if '//🐧裙：926953902' not in line]
        cleaned_json_str = '\n'.join(lines)
        
        # 重新解析 JSON 数据
        cleaned_data = json.loads(cleaned_json_str)
        
        # 替换 lives 中的 url
        if 'lives' in cleaned_data:
            for item in cleaned_data['lives']:
                if 'url' in item:
                    item['url'] = 'https://6851.kstore.space/zby.txt'
        
        # 格式化并输出修改后的 JSON 数据
        formatted_json = json.dumps(cleaned_data, indent=4, ensure_ascii=False)
        print("\n处理后的 JSON 数据:")
        print(formatted_json)
    
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")
else:
    print("响应内容为空或状态码不是 200")
