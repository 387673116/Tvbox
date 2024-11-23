@echo off
setlocal enabledelayedexpansion

:: 文件名设置
set "input_file=1.txt"   :: 输入文件名
set "output_file=2.txt"  :: 输出文件名

:: 如果输出文件已存在，则先删除
if exist "%output_file%" del "%output_file%"

:: 初始化变量
set "previous_line="

:: 读取输入文件逐行处理
for /f "delims=" %%A in (%input_file%) do (
    :: 检查当前行是否是链接
    echo %%A | findstr /i "http://" > nul
    if !errorlevel! equ 0 (
        :: 当前行是链接，测试其有效性
        curl -s -o nul -I --head "%%A"
        if !errorlevel! equ 0 (
            echo Valid: %%A
            echo !previous_line! >> "%output_file%"
            echo %%A >> "%output_file%"
        ) else (
            echo Invalid: %%A
        )
    ) else (
        :: 当前行不是链接，暂存为上一行
        set "previous_line=%%A"
    )
)

echo.
echo All valid entries saved to "%output_file%".
pause
