import ctypes
from PySide import QtGui, QtCore
import MaxPlus


def make_cylinder():
    obj = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Cylinder)
    obj.ParameterBlock.Radius.Value = 10.0
    obj.ParameterBlock.Height.Value = 30.0
    node = MaxPlus.Factory.CreateNode(obj)
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)

    return


class _GCProtector(object):
    widgets = []


app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])


def main():
    w = QtGui.QWidget()
    w.resize(250, 100)
    w.setWindowTitle('Window')
    _GCProtector.widgets.append(w)


    main_layout = QtGui.QVBoxLayout()
    label = QtGui.QLabel("Click button to create a cylinder in the scene")
    main_layout.addWidget(label)

    cylinder_btn = QtGui.QPushButton("Cylinder")
    main_layout.addWidget(cylinder_btn)
    w.setLayout(main_layout)

    cylinder_btn.clicked.connect(make_cylinder)

    w.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.MSWindowsFixedSizeDialogHint)
    w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    w.setAttribute(QtCore.Qt.WA_QuitOnClose)
    w.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDialog)

    w.move(100,500)
    w.show()

    capsule = w.effectiveWinId()
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(capsule)

    MaxPlus.Win32.Set3dsMaxAsParentWindow(ptr)


if __name__ == '__main__':
    main()