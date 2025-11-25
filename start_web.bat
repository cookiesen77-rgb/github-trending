@echo off
REM GitHub Trending Web版快速启动脚本 (Windows版本)
REM 使用方法: 双击此文件或在命令行中运行 start_web.bat

echo 🚀 启动 GitHub Trending Web版...

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

REM 启动Web服务器
echo 🌐 启动Web服务器...
echo 📍 访问地址: http://localhost:8080
echo ⏹️  按 Ctrl+C 停止服务器
echo.

python web_server.py