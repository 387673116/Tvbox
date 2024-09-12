import requests

try:
    # 下载远程 m3u 文件内容
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
        capture = False

        # 用来存储提取的内容
        result = []

        # 添加 m3u 文件头
        result.append("#EXTM3U")

        # 遍历文件的每一行
        for line in lines:
            # 检查分组行
            if line.startswith("#EXTGRP:"):
                if capture:
                    result.append("")  # 空行分隔不同分组
                result.append(line.strip())
                capture = True
                continue

            # 如果捕获状态为 True
            if capture:
                # 处理频道信息
                if line.strip() and not line.startswith("#"):
                    if "," in line:
                        # 分割频道名称和播放链接
                        channel_name, channel_url = line.split(",", 1)
                        # 添加频道信息
                        result.append(f"#EXTINF:-1,{channel_name.strip()}")
                        # 添加播放链接
                        result.append(channel_url.strip())

        # 将提取的内容写入 m3u 文件（根目录）
        with open("zb.m3u", "w", encoding="utf-8") as m3u_file:
            for r in result:
                m3u_file.write(r + "\n")

        print("zb.m3u 任务已完成.")
    else:
        print("无法下载文件")
        exit()
except Exception as e:
    print(f"发生错误: {e}")
    exit(1)
