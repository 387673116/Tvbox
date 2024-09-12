import requests
import re

def is_valid_url(url):
    # 简单的 URL 验证
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

try:
    # 下载远程m3u文件内容
    url = "https://6851.kstore.space/zby.txt"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            # 尝试以 UTF-8 编码读取内容
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            # 如果 UTF-8 解码失败，则尝试 GBK 编码
            content = response.content.decode('gbk')
        
        # 获取文件内容并按行分割
        lines = content.splitlines()

        # 定义开始标志
        start_keyword = "咪咕移动,#genre#"
        capture = False

        # 用来存储提取的内容
        result = ["#EXTM3U"]

        # 遍历文件的每一行
        for line in lines:
            # 当遇到咪咕移动时，开始捕获内容
            if start_keyword in line:
                capture = True
                continue  # 跳过标志行本身

            # 如果捕获状态为True
            if capture:
                # 如果遇到空白行或其他停止条件，可以设置结束捕获
                if line.strip() == "":
                    break

                # 每行格式为 频道名称,播放链接
                if "," in line:
                    # 分割频道名称和播放链接
                    channel_name, channel_url = line.split(",", 1)
                    # 确保 URL 有效
                    channel_url = channel_url.strip()
                    if is_valid_url(channel_url):
                        # 添加频道信息
                        result.append(f"#EXTINF:-1 group-title=\"咪咕视频\", {channel_name.strip()}")
                        # 添加播放链接
                        result.append(channel_url)

        # 将提取的内容写入m3u文件（根目录）
        with open("migutv.m3u", "w", encoding="utf-8") as m3u_file:
            for r in result:
                if r != "#EXTINF:-1 group-title=\"咪咕视频\", 咪咕视频":
                    m3u_file.write(r + "\n")

        print("migutv.m3u 任务已完成.")
    else:
        print("无法下载文件")
        exit()
except Exception as e:
    print(f"发生错误: {e}")
    exit(1)
