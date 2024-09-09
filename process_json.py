import requests

# 获取远程数据
url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json'
response = requests.get(url)

# 打印响应状态码和内容
print(f"响应状态码: {response.status_code}")
print("响应内容:")
print(response.text)

# 检查响应是否成功且内容是否为空
if response.status_code == 200 and response.text.strip():
    # 删除包含特定字符串的行
    lines = response.text.split('\n')
    lines = [line for line in lines if '//🐧裙：926953902' not in line]
    cleaned_text = '\n'.join(lines)

    # 替换特定 URL
    replaced_text = cleaned_text.replace('https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt', 'https://6851.kstore.space/zby.txt')

    # 打印替换后的文本
    print("\n替换后的文本:")
    print(replaced_text)
else:
    print("响应内容为空或状态码不是 200")
