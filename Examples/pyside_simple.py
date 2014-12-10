from PySide import QtGui, QtCore, shiboken

import MaxPlus


def make_cylinder():
    obj = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Cylinder)
    obj.ParameterBlock.Radius.Value = 10.0
    obj.ParameterBlock.Height.Value = 30.0
    MaxPlus.Factory.CreateNode(obj)
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)

    return


class _GCProtector(object):
    controls = []


def main():
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    mainWindow = QtGui.QMainWindow()
    _GCProtector.controls.append(mainWindow)
    mainWindow.setWindowTitle('Simple tool')
    mainWindow.resize(250,50)

    widget = QtGui.QWidget()

    main_layout = QtGui.QVBoxLayout()
    label = QtGui.QLabel("Click button to create a cylinder in the scene")
    main_layout.addWidget(label)

    cylinder_btn = QtGui.QPushButton("Cylinder")
    main_layout.addWidget(cylinder_btn)
    widget.setLayout(main_layout)

    mainWindow.setCentralWidget(widget)

    cylinder_btn.clicked.connect(make_cylinder)

    mainWindow.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.MSWindowsFixedSizeDialogHint)
    mainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    mainWindow.setAttribute(QtCore.Qt.WA_QuitOnClose)
    mainWindow.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDialog)

    mainWindow.show()

if __name__ == '__main__':
    main()