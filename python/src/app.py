import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import pymysql.cursors
from jinja2 import Template, Environment, FileSystemLoader

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = pymysql.connect(host='mysql',
                    user='root',
                    password='password',
                    db='ctf_db',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
        try:
            url = urlparse(self.path)

            if url.path == '/':
                params = parse_qs(url.query)
                query = params.get('q', [''])[0]
                
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM users WHERE delete_flag=FALSE AND job LIKE '%" + query + "%'"    
                    cursor.execute(sql)
                    result = cursor.fetchall()

                env = Environment(loader=FileSystemLoader('.'))
                template = env.get_template('index.html')
                
                data = {
                    'query': query,
                    'result': result
                }
                disp_text = template.render(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(disp_text.encode('utf-8'))
            else:
                self.send_response(404)
        except Exception as e:
            print(e)

            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(str(e).encode('utf-8'))
        finally:
            conn.close()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
