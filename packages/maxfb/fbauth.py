import urlparse
import BaseHTTPServer
import webbrowser

ACCESS_TOKEN = None
auth_url = 'http://www.youcandoitvfx.com/fb/'
server_host = '127.0.0.1'
server_port = 80


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_TOKEN

        self.send_response(301)
        self.send_header('Location', auth_url + 'close.html')
        self.end_headers()

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        _access_token = params.get('access_token', 'error')
        if (_access_token != 'error') and (len(_access_token) != 0):
            ACCESS_TOKEN = _access_token

def getAccessToken():
    global ACCESS_TOKEN

    ACCESS_TOKEN = None

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((server_host, server_port), MyHandler)
    webbrowser.open(auth_url)
    while ACCESS_TOKEN is None:
        httpd.handle_request()

    httpd.server_close()

    return ACCESS_TOKEN