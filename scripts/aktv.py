import requests
from bs4 import BeautifulSoup

# 获取网页内容
def fetch_channels(url="https://aktv.top/"):
    """抓取网页并提取频道信息"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    channels = []
    for item in soup.find_all('div', class_='channel-class'):  # 需要根据实际网页结构修改
        title = item.find('span', class_='title').text.strip()
        link = item.find('a', href=True)['href'].strip()
        category = item.find('span', class_='category').text.strip()
        tv_id = item.get('tv-id', 'unknown')  # 获取tv-id属性，若没有则为unknown

        # 添加频道信息
        channels.append((category, title, link, tv_id))
    
    return channels

# 检查链接有效性
def is_valid_url(url):
    """检查URL是否有效"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# 保存到.m3u文件
def save_to_m3u(channels, filename="guoji.m3u"):
    """将有效的频道链接保存到.m3u文件中"""
    with open(filename, "w", encoding="utf-8") as file:
        for category, title, link, tv_id in channels:
            # 验证链接有效性
            if is_valid_url(link):
                file.write(f'#EXTINF:-1 group-title="{category}", {title} (ID: {tv_id})\n')
                file.write(f'{link}\n')

# 主函数
def main():
    url = "https://aktv.top/"
    
    # 1. 获取频道信息
    channels = fetch_channels(url)
    
    # 2. 保存有效的链接到.m3u文件
    save_to_m3u(channels)

if __name__ == "__main__":
    main()
