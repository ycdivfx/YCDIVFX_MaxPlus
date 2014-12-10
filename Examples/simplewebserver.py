import BaseHTTPServer
import cgi
import ctypes
import os
import sys
import threading

from PySide import QtGui

import MaxPlus

PORT = 8000


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exiting = False

        address = ('localhost', PORT)
        self.server = BaseHTTPServer.HTTPServer(address, MyHandler)
        self._stop = threading.Event()

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.server_close()
        self.server.shutdown()
        self._stop.set()



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        rootdir = os.path.join(os.path.dirname(__file__) + '/html')
        try:
            if self.path == '/':
                self.path = '/index.html'
            if self.path.endswith('.html'):

                self.send_response(200)
                self.send_header('Content-type','text-html')
                self.end_headers()

                f = open(rootdir + self.path)
                self.wfile.write(f.read())
                f.close()
                return

        except IOError:
            self.send_error(404, 'file not found')

    def do_POST(self):
        if self.path=="/cmd":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })

            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
            try:
                MaxPlus.Core.EvalMAXScript(form["cmd"].value)
                MaxPlus.ViewportManager_ForceCompleteRedraw()
            except:
                print "Needs to be run from a 3ds max instance"
        return


class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowTitle('Simple 3ds Max webserver')
        self.resize(200,50)
        self.btn_run = QtGui.QPushButton('Run')
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.btn_run)
        self.setLayout(layout)
        self.btn_run.clicked.connect(self.run)

        self.serverThread = None

    def run(self):
        if not self.serverThread:
            print "Serving at port", PORT
            self.btn_run.setText('Stop...')
            self.serverThread = MyThread()
            self.serverThread.start()
        else:
            print "Stopping webserver"
            self.btn_run.setText('Run')
            self.serverThread.stop()
            self.serverThread = None

    def closeEvent(self, *args, **kwargs):
        if self.serverThread:
            print "Stopping webserver"
            self.btn_run.setText('Run')
            self.serverThread.stop()
            self.serverThread = None

class _GCProtector(object):
    controls = []


if __name__ == '__main__':
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    window = MyWindow()
    _GCProtector.controls.append(window)
    window.show()

    capsule = window.effectiveWinId()
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(capsule)

    MaxPlus.Win32.Set3dsMaxAsParentWindow(ptr)

