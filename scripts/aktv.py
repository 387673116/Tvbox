from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests

# 设置 Chrome 无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
chrome_options.add_argument("--no-sandbox")  # 解决一些环境问题

# 启动 Chrome 浏览器
driver = webdriver.Chrome(options=chrome_options)

# 打开目标网页
driver.get("http://aktv.top/")

# 等待页面加载完成
time.sleep(5)  # 或者使用 WebDriverWait 等待特定元素加载

# 获取所有链接
links = driver.find_elements(By.TAG_NAME, 'a')

# 保存有效的 m3u8 链接
valid_links = []
for link in links:
    href = link.get_attribute('href')
    if href and "m3u8" in href:  # 检查链接是否包含 m3u8
        if requests.head(href).status_code == 200:  # 检查链接是否有效
            valid_links.append(href)

# 关闭浏览器
driver.quit()

# 输出结果并保存到 guoji.m3u 文件
with open("guoji.m3u", "w", encoding="utf-8") as file:
    for link in valid_links:
        file.write(f"#EXTINF:-1 group-title=\"国际\", {link}\n")
        file.write(f"{link}\n")

print("m3u文件更新完成")
