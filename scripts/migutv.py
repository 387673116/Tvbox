import requests

try:
    # 下载远程txt文件内容
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

        # 定义开始标志和结束条件
        start_keyword = "咪咕移动,#genre#"

        # 用来存储提取的内容
        result = []
        capture = False

        # 遍历文件的每一行
        for line in lines:
            # 如果遇到开始标志
            if start_keyword in line:
                capture = True
                result.append(line.strip())  # 保留“咪咕移动,#genre#”这一行

            # 如果处于提取状态
            elif capture:
                # 遇到空白行时停止提取
                if line.strip() == "":
                    break
                result.append(line.strip())  # 添加到结果

        # 将提取的内容写入TXT文件（根目录）
        with open("migutv.txt", "w", encoding="utf-8") as txt_file:
            for r in result:
                txt_file.write(r + "\n")

        print("File migutv.txt has been written successfully.")
    else:
        print("无法下载文件")
        exit()
except Exception as e:
    print(f"发生错误: {e}")
    exit(1)
