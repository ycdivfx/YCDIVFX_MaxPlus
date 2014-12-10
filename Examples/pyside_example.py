import ctypes

from PySide import QtGui, QtCore

import MaxPlus


def make_cylinder():
    obj = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Cylinder)
    obj.ParameterBlock.Radius.Value = 10.0
    obj.ParameterBlock.Height.Value = 30.0
    MaxPlus.Factory.CreateNode(obj)
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)


class Widget(QtGui.QWidget):
    def __init__(self, parent=None, stylename='windows', theme='dark'):
        super(Widget, self).__init__(parent)

        self.btnRun  = QtGui.QPushButton('Run')
        self.btnClose = QtGui.QPushButton('Close')

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.btnRun)
        layout.addWidget(self.btnClose)
        self.setLayout(layout)
        self.setWindowTitle('Simple 3ds Max PySide Example')

        self.setWindowFlags(QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.btnRun.clicked.connect(make_cylinder)
        self.btnClose.clicked.connect(self.close)
        self.setGeometry(100, 100, 250, 80)
        print self.frameGeometry()

        self.setupUI(stylename, theme)

    def setupUI(self, stylename, theme):
        for control in self.children():
             if hasattr(control, 'setStyle'):
                control.setStyle(QtGui.QStyleFactory.create(stylename))

        if theme.lower() == 'dark':
            self.setStyleSheet('QWidget {'
                               'background: #444444;'
                               'color: #d8d8d8;'
                               'selection-color: black;'
                               'selection-background-color: #3399ff;'
                               '}')
        else:
            self.setStyleSheet('QWidget {'
                               'background: #E6E6E6;'
                               'color: #000000;'
                               'selection-color: black;'
                               'selection-background-color: #3399ff;'
                               '}')


class _GCProtector(object):
    widgets = []


app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])


def main():
    widget = Widget(stylename='Plastique', theme='light')
    _GCProtector.widgets.append(widget)
    widget.show()

    capsule = widget.effectiveWinId()
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(capsule)

    MaxPlus.Win32.Set3dsMaxAsParentWindow(ptr)

if __name__ == '__main__':
    main()