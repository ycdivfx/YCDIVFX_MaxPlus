import os
import urlparse
import BaseHTTPServer
import webbrowser
import requests

access_token = None
success = False
auth_url = 'http://www.youcandoitvfx.com/fb/'
local_file = '.fb_access_token'
server_host = '127.0.0.1'
server_port = 80


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token, success
        """Respond to a GET request."""
        self.send_response(301)
        self.send_header('Location', auth_url + 'close.html')
        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        access_token = params.get('access_token', 'error')
        if (access_token != 'error') and (len(access_token) != 0):

            self.wfile.write(access_token)
            success = True
        else:
            success = False


def checktokenstatus(local_file):
    if os.path.exists(local_file):
        local_token = open(local_file).read()
        r = requests.get('https://graph.facebook.com/debug_token',
                         params={'input_token' : local_token, 'access_token' : local_token})
        data = r.json()
        if 'error' in data:
            return True
    return False


def getaccesstoken():
    global access_token, success

    if checktokenstatus(local_file):
        os.remove(local_file)

    if os.path.exists(local_file):
            access_token = open(local_file).read()
    else:
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((server_host, server_port), MyHandler)
        webbrowser.open(auth_url)
        while access_token is None:
            httpd.handle_request()
        if success:
            open(local_file,'w').write(access_token)
        httpd.server_close()

    return access_token