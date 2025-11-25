#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending CLI Tool
抓取GitHub热门仓库并在终端以简洁美观的形式显示
Fetch GitHub trending repositories and display them beautifully in terminal
"""

import warnings
warnings.filterwarnings('ignore')

import requests
from bs4 import BeautifulSoup
import sys
import os
from datetime import datetime

# ==================== 跨平台颜色支持 ====================
def init_colors():
    """初始化终端颜色支持（Windows兼容）"""
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        return True
    except ImportError:
        # Windows without colorama - try to enable ANSI
        if os.name == 'nt':
            os.system('')  # Enable ANSI on Windows 10+
        return False

# Initialize colors
init_colors()

# ==================== 颜色常量定义 ====================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 前景色
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 加粗前景色
    BOLD_RED = '\033[1;31m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_CYAN = '\033[1;36m'


# ==================== 核心抓取函数 ====================

def fetch_trending_html(since='daily'):
    """
    抓取GitHub Trending页面HTML
    
    Args:
        since: 时间范围 (daily/weekly/monthly)
    
    Returns:
        str: HTML内容，失败返回None
    """
    url = f'https://github.com/trending?since={since}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return None


def parse_repo(article):
    """
    解析单个仓库的HTML元素
    
    Args:
        article: BeautifulSoup Tag对象
    
    Returns:
        dict: 仓库信息字典
    """
    try:
        # 仓库名称和链接
        name_elem = article.select_one('h2 a')
        if not name_elem:
            return None
        
        href = name_elem.get('href', '').strip()
        name = href.lstrip('/')
        url = f'https://github.com{href}'
        
        # 描述
        desc_elem = article.select_one('p')
        description = desc_elem.get_text(strip=True) if desc_elem else ''
        
        # 总星标数
        stars = ''
        stars_elem = article.select_one('a[href$="/stargazers"]')
        if stars_elem:
            stars = stars_elem.get_text(strip=True)
        
        # 今日/本周/本月新增星标
        today_stars = ''
        today_elem = article.select_one('span.d-inline-block.float-sm-right')
        if today_elem:
            today_stars = today_elem.get_text(strip=True)
        
        # 编程语言
        language = ''
        lang_elem = article.select_one('span[itemprop="programmingLanguage"]')
        if lang_elem:
            language = lang_elem.get_text(strip=True)
        
        return {
            'name': name,
            'url': url,
            'description': description,
            'stars': stars,
            'today_stars': today_stars,
            'language': language
        }
    
    except Exception:
        return None


def get_trending_data(since='daily'):
    """
    获取GitHub Trending数据（供Web和CLI使用）
    
    Args:
        since: 时间范围 (daily/weekly/monthly)
    
    Returns:
        dict: {'success': bool, 'data': list, 'error': str}
    """
    html = fetch_trending_html(since)
    
    if not html:
        return {
            'success': False,
            'data': [],
            'error': 'Failed to fetch GitHub Trending page'
        }
    
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('article.Box-row')
    
    if not articles:
        return {
            'success': False,
            'data': [],
            'error': 'No repositories found, GitHub page structure may have changed'
        }
    
    repos = []
    for article in articles:
        repo = parse_repo(article)
        if repo:
            repos.append(repo)
    
    return {
        'success': True,
        'data': repos,
        'error': None
    }


# ==================== CLI显示函数 ====================

def print_header(since):
    """
    打印美观的标题头
    
    Args:
        since: 时间范围
    """
    since_map = {
        'daily': 'Daily (今日)',
        'weekly': 'Weekly (本周)',
        'monthly': 'Monthly (本月)'
    }
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    title = f"🔥 GitHub Trending - {since_map.get(since, since)} | {date_str}"
    
    width = 66
    print()
    print(f'{Colors.BOLD_CYAN}╔{"═" * width}╗{Colors.RESET}')
    print(f'{Colors.BOLD_CYAN}║{Colors.BOLD_YELLOW}{title:^{width}}{Colors.BOLD_CYAN}║{Colors.RESET}')
    print(f'{Colors.BOLD_CYAN}╚{"═" * width}╝{Colors.RESET}')
    print()


def print_repo(index, repo):
    """
    带颜色打印单个仓库信息
    
    Args:
        index: 序号
        repo: 仓库信息字典
    """
    # 第一行：序号 + 仓库名
    print(f" {Colors.BOLD}{index:>2}.{Colors.RESET} {Colors.BOLD_BLUE}{repo['name']}{Colors.RESET}")
    
    # 第二行：描述
    desc = repo['description'] if repo['description'] else 'No description'
    if len(desc) > 80:
        desc = desc[:77] + '...'
    print(f"     {Colors.WHITE}{desc}{Colors.RESET}")
    
    # 第三行：语言 + 星标
    lang_display = f"{Colors.CYAN}[{repo['language']}]{Colors.RESET} " if repo['language'] else ''
    stars_display = f"⭐ {repo['stars']}" if repo['stars'] else ''
    
    # 处理今日新增
    today_display = ''
    if repo['today_stars']:
        today_text = repo['today_stars']
        # 提取数字
        for suffix in [' stars today', ' stars this week', ' stars this month']:
            today_text = today_text.replace(suffix, '')
        today_display = f" {Colors.BOLD_GREEN}(+{today_text}){Colors.RESET}"
    
    print(f"     {lang_display}{Colors.YELLOW}{stars_display}{Colors.RESET}{today_display}")
    
    # 第四行：链接（红色高亮）
    print(f"     {Colors.BOLD_RED}🔗 {repo['url']}{Colors.RESET}")
    print()


def print_usage():
    """打印使用说明"""
    print(f'''
{Colors.BOLD_CYAN}GitHub Trending CLI Tool{Colors.RESET}

{Colors.BOLD}Usage:{Colors.RESET}
  python github_trend.py [option]

{Colors.BOLD}Options:{Colors.RESET}
  daily   - Today's trending (default)
  weekly  - This week's trending
  monthly - This month's trending
  -h, --help - Show this help message

{Colors.BOLD}Examples:{Colors.RESET}
  python github_trend.py          # Today's trending
  python github_trend.py daily    # Today's trending
  python github_trend.py weekly   # This week's trending
  python github_trend.py monthly  # This month's trending
''')


def main():
    """主函数"""
    # 处理命令行参数
    valid_options = ['daily', 'weekly', 'monthly']
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['-h', '--help', 'help']:
            print_usage()
            sys.exit(0)
        elif arg in valid_options:
            since = arg
        else:
            print(f'{Colors.BOLD_RED}✗ Invalid option: {arg}{Colors.RESET}')
            print(f'  Valid options: {", ".join(valid_options)}')
            sys.exit(1)
    else:
        since = 'daily'
    
    # 打印标题
    print_header(since)
    
    # 抓取数据
    print(f'{Colors.CYAN}Fetching data...{Colors.RESET}\n')
    result = get_trending_data(since)
    
    if not result['success']:
        print(f'{Colors.BOLD_RED}✗ {result["error"]}{Colors.RESET}')
        sys.exit(1)
    
    repos = result['data']
    if not repos:
        print(f'{Colors.BOLD_YELLOW}No repositories found{Colors.RESET}')
        sys.exit(1)
    
    # 清除"正在抓取"提示
    print('\033[2A\033[K', end='')
    
    # 打印仓库列表
    for i, repo in enumerate(repos, 1):
        print_repo(i, repo)
    
    # 打印统计
    print(f'{Colors.BOLD_CYAN}{"─" * 68}{Colors.RESET}')
    print(f'{Colors.BOLD}Total: {len(repos)} trending repositories{Colors.RESET}')
    print()


if __name__ == '__main__':
    main()
