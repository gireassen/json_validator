from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
from pathlib import Path

PORT = 8000
TEMPLATES_DIR = Path(__file__).parent / 'templates'
STATIC_DIR = Path(__file__).parent / 'static'

class JSONValidatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            with open(TEMPLATES_DIR / 'index.html', 'r', encoding='utf-8') as f:
                html = f.read()
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path.startswith('/static/'):
            try:
                static_file = STATIC_DIR / self.path[8:]
                if static_file.is_file():
                    self.send_response(200)
                    if self.path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif self.path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    
                    with open(static_file, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "File not found")
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        json_data = params.get('json_data', [''])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        try:
            parsed = json.loads(json_data)
            formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
            result_html = f"""
            <div class="success">
                <h3>✓ Valid JSON</h3>
                <pre>{formatted}</pre>
            </div>
            """
            error_line = None
            error_pos = None
        except json.JSONDecodeError as e:
            error_line = 1
            error_pos = e.pos
            
            if error_pos is not None:
                lines = json_data.split('\n')
                pos_counter = 0
                
                for i, line in enumerate(lines):
                    if pos_counter + len(line) >= error_pos:
                        error_line = i + 1
                        break
                    pos_counter += len(line) + 1
            
            # Generate error context
            lines = json_data.split('\n')
            start_line = max(0, error_line - 3)
            end_line = min(len(lines), error_line + 2)
            
            error_context = []
            for i in range(start_line, end_line):
                line_num = i + 1
                line_content = lines[i]
                
                if line_num == error_line:
                    error_context.append(f"""
                    <div class="error-line">
                        <span class="line-number">{line_num}:</span> {line_content}
                    </div>
                    """)
                else:
                    error_context.append(f"""
                    <div>
                        <span class="line-number">{line_num}:</span> {line_content}
                    </div>
                    """)
            
            result_html = f"""
            <div class="error">
                <h3>✗ Invalid JSON</h3>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Tip:</strong> Проверьте отсутствие запятых между элементами объекта, 
                незакрытые кавычки или скобки.</p>
                
                <div class="error-context">
                    <h4>Error context:</h4>
                    {"".join(error_context)}
                </div>
            </div>
            """

        with open(TEMPLATES_DIR / 'result.html', 'r', encoding='utf-8') as f:
            html = f.read().format(
                json_data=json_data,
                result=result_html,
                error_line=error_line if 'error_line' in locals() else 'null',
                error_pos=error_pos if 'error_pos' in locals() else 'null'
            )
        
        self.wfile.write(html.encode('utf-8'))

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, JSONValidatorHandler)
    print(f"Server running on http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()