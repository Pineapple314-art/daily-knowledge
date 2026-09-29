"""
每日杂学 - 本地服务器
同时提供静态文件服务和 AI API 代理功能
"""

import http.server
import socketserver
import os
import urllib.parse
import urllib.request
import json

PORT = 8090
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DailyKnowledgeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # AI 代理端点
        if self.path.startswith('/api/ask'):
            self.handle_ai_request()
        else:
            # 添加 no-cache 头
            super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def handle_ai_request(self):
        """代理 AI 请求到 Pollinations"""
        try:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            prompt = params.get('prompt', [''])[0]
            model = params.get('model', ['openai'])[0]

            if not prompt:
                self.send_json(400, {'error': '缺少 prompt 参数'})
                return

            # URL 编码 prompt 并构建 Pollinations URL
            encoded_prompt = urllib.parse.quote(prompt)
            ai_url = f'https://text.pollinations.ai/{encoded_prompt}?model={model}'

            # 创建请求，模拟浏览器请求
            req = urllib.request.Request(ai_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('Accept', 'text/plain, */*')

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read().decode('utf-8')
                self.send_json(200, {'content': content, 'status': 'ok'})

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='replace')
            self.send_json(e.code, {'error': f'HTTP {e.code}', 'detail': error_body[:500]})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # 静默日志（可选：取消注释来调试）
        pass

if __name__ == '__main__':
    with socketserver.TCPServer(('0.0.0.0', PORT), DailyKnowledgeHandler) as httpd:
        print(f'每日杂学服务器运行在 http://localhost:{PORT}')
        print(f'打开浏览器访问 http://localhost:{PORT}')
        httpd.serve_forever()
