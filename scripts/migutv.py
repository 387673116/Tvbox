import requests

def fetch_m3u_file(url):
    try:
        # 下载远程m3u文件内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        try:
            # 尝试以 UTF-8 编码读取内容
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            # 如果 UTF-8 解码失败，则尝试 GBK 编码
            content = response.content.decode('gbk')

        return content

    except requests.RequestException as e:
        print(f"请求错误: {e}")
        exit(1)

def process_m3u_content(content):
    # 获取文件内容并按行分割
    lines = content.splitlines()

    # 定义开始标志
    start_keyword = "咪咕移动,#genre#"
    capture = False

    # 用来存储提取的内容
    result = []

    # 添加m3u文件头
    result.append("#EXTM3U")

    # 添加分类名称
    category_name = "咪咕视频"
    result.append(f"#EXTINF:-1 group-title=\"{category_name}\", {category_name}")

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
                # 添加频道信息
                result.append(f"#EXTINF:-1 group-title=\"{category_name}\", {channel_name.strip()}")
                # 添加播放链接
                result.append(channel_url.strip())

    return result

def write_m3u_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as m3u_file:
            for line in content:
                m3u_file.write(line + "\n")
        print(f"{filename} 任务已完成.")
    except IOError as e:
        print(f"文件操作错误: {e}")
        exit(1)

def main():
    url = "https://6851.kstore.space/zby.txt"
    content = fetch_m3u_file(url)
    processed_content = process_m3u_content(content)
    write_m3u_file("migutv.m3u", processed_content)

if __name__ == "__main__":
    main()
