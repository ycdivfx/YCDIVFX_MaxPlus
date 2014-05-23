from PySide import QtGui, QtCore

import MaxPlus

from maxui import MaxWindow


def make_cylinder():
    obj = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Cylinder)
    obj.ParameterBlock.Radius.Value = 10.0
    obj.ParameterBlock.Height.Value = 30.0
    MaxPlus.Factory.CreateNode(obj)
    time = MaxPlus.Core.GetCurrentTime()
    MaxPlus.ViewportManager.RedrawViews(time)


@MaxWindow
class Widget(QtGui.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        self.btnRun = QtGui.QPushButton('Run')
        self.btnClose = QtGui.QPushButton('Close')

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.btnRun)
        layout.addWidget(self.btnClose)
        self.setLayout(layout)
        self.setWindowTitle('Simple 3ds Max PySide Example')

        self.setWindowFlags(QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.btnRun.clicked.connect(make_cylinder)
        self.btnClose.clicked.connect(self.close)
        self.setGeometry(100, 100, 250, 80)
        print self.frameGeometry()


app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])


def main():
    widget = Widget(parented=True)
    widget.show()

if __name__ == '__main__':
    main()
