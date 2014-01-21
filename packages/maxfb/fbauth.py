import os
import urlparse
import BaseHTTPServer
import webbrowser
import requests

access_token = None
auth_url = 'http://www.youcandoitvfx.com/fb/'
local_file = r'.fb_access_token'
server_host = '127.0.0.1'
server_port = 80


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        _access_token = params.get('access_token', 'error')
        if (_access_token != 'error') and (len(_access_token) != 0):
            access_token = _access_token

        self.wfile.write("""<html>
                            <head>
                            <title>Close</title>
                            <script type=\"text/javascript\">
                            function closeMe(){
                              window.open(\"\",\"_self\");
                              window.close();
                            }
                            closeMe();
                            </script>
                            </head>
                            <body>
                            </body>
                            </html>""")


def getAccessToken():
    global access_token

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((server_host, server_port), MyHandler)
    webbrowser.open(auth_url)
    while access_token is None:
        httpd.handle_request()

    httpd.server_close()

    return access_token