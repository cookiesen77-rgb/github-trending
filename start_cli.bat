@echo off
REM GitHub Trending CLI版快速启动脚本 (Windows版本)
REM 使用方法: start_cli.bat [daily|weekly|monthly]

echo 🔥 启动 GitHub Trending CLI版...

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate

REM 检查依赖是否已安装
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 安装依赖包...
    pip install -r requirements.txt
)

REM 运行CLI程序
echo 🖥️ 运行CLI程序...
echo.

REM 传递命令行参数给程序
python github_trend.py %1 %2 %3