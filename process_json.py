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
    cleaned_text = re.sub(r'//🐧裙：926953902', '', text)

    # 替换特定 URL
    cleaned_text = cleaned_text.replace(
        'https://github.moeyy.xyz/https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt',
        'https://6851.kstore.space/zby.txt'
    )

    # 替换 "豆瓣┃本接口免费-🈲贩卖" 为 "豆瓣TOP榜"
    cleaned_text = cleaned_text.replace('豆瓣┃本接口免费-🈲贩卖', '豆瓣TOP榜')

    # 处理"lives"之前的部分内容
    if '"lives":' in cleaned_text:
        # 获取 "lives" 之前的所有内容
        pre_lives_content = cleaned_text.split('"lives":')[0]

        # 定义需要删除的关键字列表
        keywords = ['虎牙直播', '有声小说吧', '88看球', '少儿', '小学', '初中', 'TgYunPan', 
                    '高中', '急救教学', '易搜', '网盘', '纸条', '（墙外）', '搜索', '易搜', '本地', '推送', '动漫', '动漫']

        # 构建正则表达式，删除包含指定关键字的 {} 块，处理跨行情况
        for keyword in keywords:
            # 使用 DOTALL 模式 (re.S)，让 `.` 匹配所有字符，包括换行符
            pattern = r'\{[^{}]*' + re.escape(keyword) + r'[^{}]*\},?'
            pre_lives_content = re.sub(pattern, '', pre_lives_content, flags=re.S)

        # 将处理后的内容与 "lives" 后面的部分重新拼接
        post_lives_content = cleaned_text.split('"lives":', 1)[1]
        cleaned_text = pre_lives_content + '"lives":' + post_lives_content

    # 打印处理后的文本
    print("\n处理后的文本:")
    print(cleaned_text)

else:
    print("响应内容为空或状态码不是 200")
