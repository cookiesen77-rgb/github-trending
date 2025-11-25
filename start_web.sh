#!/bin/bash

# GitHub Trending Web版快速启动脚本
# 使用方法: ./start_web.sh

echo "🚀 启动 GitHub Trending Web版..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否已安装
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 安装依赖包..."
    pip install -r requirements.txt
fi

# 启动Web服务器
echo "🌐 启动Web服务器..."
echo "📍 访问地址: http://localhost:8080"
echo "⏹️  按 Ctrl+C 停止服务器"
echo ""

python3 web_server.py