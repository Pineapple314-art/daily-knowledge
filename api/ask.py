"""
每日杂学 - AI 问答代理 (Vercel Serverless Function)
将前端请求转发到 Pollinations AI 接口，避免 CORS 和地域限制
"""

from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import json


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            prompt = params.get('prompt', [''])[0]
            model = params.get('model', ['openai'])[0]

            if not prompt:
                self._send_json(400, {'error': '缺少 prompt 参数'})
                return

            encoded_prompt = urllib.parse.quote(prompt)
            ai_url = f'https://text.pollinations.ai/{encoded_prompt}?model={model}'

            req = urllib.request.Request(ai_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            req.add_header('Accept', 'text/plain, */*')

            with urllib.request.urlopen(req, timeout=55) as response:
                content = response.read().decode('utf-8')
                self._send_json(200, {'content': content, 'status': 'ok'})

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='replace')
            self._send_json(e.code, {'error': f'HTTP {e.code}', 'detail': error_body[:500]})
        except Exception as e:
            self._send_json(500, {'error': str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
