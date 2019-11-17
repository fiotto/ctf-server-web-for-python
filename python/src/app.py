import http.server
import socketserver

from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse
import urllib

from jinja2 import Template, Environment, FileSystemLoader
import pymysql.cursors

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = None
        conn = pymysql.connect(host='mysql',
                    user='root',
                    password='password',
                    db='ctf_db',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)

        try:
            url = urlparse(self.path)
            if url.path == '/':
                params = urllib.parse.parse_qs(url.query)
                query = params.get('q', [''])[0]
                print('query')
                print(url)
                print(url.query)
                print(query)
                print('----------')

                try:
                    with conn.cursor() as cursor:
                        sql = "SELECT * FROM users"
                        sql = "SELECT * FROM users WHERE delete_flag=FALSE AND job LIKE '%" + query + "%'"    
                        print(sql)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        print(result)
                finally:
                    conn.close()

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

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()