#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending Web Server
本地Web服务器，在浏览器中展示GitHub热门仓库
Local web server to display GitHub trending repositories in browser
"""

import webbrowser
import threading
import sys
import os

# Add current directory to path for importing github_trend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, jsonify, request
from github_trend import get_trending_data

app = Flask(__name__)

# ==================== Routes ====================

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/trending')
def api_trending():
    """
    API endpoint for fetching trending data
    
    Query Parameters:
        since: daily | weekly | monthly (default: daily)
    
    Returns:
        JSON: {success: bool, data: list, error: str|null}
    """
    since = request.args.get('since', 'daily')
    
    # Validate parameter
    if since not in ['daily', 'weekly', 'monthly']:
        return jsonify({
            'success': False,
            'data': [],
            'error': f'Invalid parameter: since={since}. Valid options: daily, weekly, monthly'
        }), 400
    
    # Fetch data
    result = get_trending_data(since)
    
    return jsonify(result)


# ==================== Helper Functions ====================

def open_browser(port):
    """Open browser after a short delay"""
    def _open():
        import time
        time.sleep(1.5)
        webbrowser.open(f'http://localhost:{port}')
    
    thread = threading.Thread(target=_open)
    thread.daemon = True
    thread.start()


def print_banner(port):
    """Print startup banner"""
    print('''
╔══════════════════════════════════════════════════════════════════╗
║                   🔥 GitHub Trending Web Server                  ║
╚══════════════════════════════════════════════════════════════════╝
''')
    print(f'  🌐 Local:   http://localhost:{port}')
    print(f'  🌐 Network: http://0.0.0.0:{port}')
    print()
    print('  Press Ctrl+C to stop the server')
    print()


# ==================== Main ====================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub Trending Web Server')
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='Port to run the server on (default: 8080)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open browser automatically')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner(args.port)
    
    # Open browser
    if not args.no_browser:
        open_browser(args.port)
    
    # Run server
    try:
        app.run(
            host='0.0.0.0',
            port=args.port,
            debug=args.debug,
            use_reloader=args.debug
        )
    except KeyboardInterrupt:
        print('\n\n  👋 Server stopped. Goodbye!')


if __name__ == '__main__':
    main()

