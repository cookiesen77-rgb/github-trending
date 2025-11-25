#!/bin/bash

# GitHub Trending CLI版快速启动脚本
# 使用方法: ./start_cli.sh [daily|weekly|monthly]

echo "🔥 启动 GitHub Trending CLI版..."

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

# 运行CLI程序
echo "🖥️ 运行CLI程序..."
echo ""

# 传递命令行参数给程序
python3 github_trend.py "$@"