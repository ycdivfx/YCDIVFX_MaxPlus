import urlparse
import BaseHTTPServer
import webbrowser

ACCESS_TOKEN = None
auth_url = 'http://www.youcandoitvfx.com/fb/'
local_file = '.fb_access_token'
server_host = '127.0.0.1'
server_port = 80


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_TOKEN

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
            ACCESS_TOKEN = _access_token

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
    global ACCESS_TOKEN

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((server_host, server_port), MyHandler)
    webbrowser.open(auth_url)
    while ACCESS_TOKEN is None:
        httpd.handle_request()

    httpd.server_close()

    return ACCESS_TOKEN