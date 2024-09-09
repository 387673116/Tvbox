import requests
import json

# 获取远程 JSON 数据
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")
print("响应内容:")
print(response.text)

# 检查响应是否成功且内容是否为空
if response.status_code == 200 and response.text.strip():
    try:
        # 解析 JSON 数据
        data = response.json()

        # 将数据转换为字符串形式进行处理
        json_str = json.dumps(data, ensure_ascii=False)

        # 打印原始 JSON 字符串
        print("原始 JSON 字符串:")
        print(json_str)

        # 删除包含特定字符串的行（这里我们假设删除操作是在 JSON 字符串中进行）
        lines = json_str.split('\n')
        lines = [line for line in lines if '//🐧裙：926953902' not in line]
        cleaned_json_str = '\n'.join(lines)

        # 打印清理后的 JSON 字符串
        print("\n清理后的 JSON 字符串:")
        print(cleaned_json_str)
        
        # 重新将清理后的 JSON 字符串解析为 Python 对象
        cleaned_data = json.loads(cleaned_json_str)
        
        # 格式化并输出清理后的 JSON 数据
        formatted_json = json.dumps(cleaned_data, indent=4, ensure_ascii=False)
        print("\n格式化后的 JSON 数据:")
        print(formatted_json)
    
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")
else:
    print("响应内容为空或状态码不是 200")
