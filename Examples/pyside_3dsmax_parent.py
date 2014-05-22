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


class _GCProtector(object):
    controls = []


def main():
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    widget = QtGui.QWidget()
    _GCProtector.controls.append(widget)
    widget.setWindowTitle('Simple tool')
    widget.resize(250,50)

    main_layout = QtGui.QVBoxLayout()
    label = QtGui.QLabel("Click button to create a cylinder in the scene")
    main_layout.addWidget(label)

    cylinder_btn = QtGui.QPushButton("Cylinder")
    main_layout.addWidget(cylinder_btn)
    widget.setLayout(main_layout)

    cylinder_btn.clicked.connect(make_cylinder)

    widget.setWindowFlags(QtCore.Qt.Tool |
                          QtCore.Qt.WindowStaysOnTopHint |
                          QtCore.Qt.MSWindowsFixedSizeDialogHint)
    widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    widget.setAttribute(QtCore.Qt.WA_QuitOnClose)
    widget.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDialog)

    widget.show()

    capsule = widget.effectiveWinId()
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(capsule)

    MaxPlus.Win32.Set3dsMaxAsParentWindow(ptr)

if __name__ == '__main__':
    main()