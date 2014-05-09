import os
from PySide import QtGui

import MaxPlus


class MyWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.lbl_project = QtGui.QLabel('Project Path...')
        self.btn_project = QtGui.QPushButton('Select project folder')
        self.txt_prefix = QtGui.QLineEdit()
        self.btn_run = QtGui.QPushButton('Run')

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.lbl_project)
        layout.addWidget(self.btn_project)
        layout.addWidget(self.txt_prefix)
        layout.addWidget(self.btn_run)
        self.setLayout(layout)

        self.txt_prefix.setText('whatever_')

        self.btn_project.clicked.connect(self.select_project_folder)
        self.btn_run.clicked.connect(self.addCache)

        self.setupPaths()
        self.updateUI()

    def setupPaths(self):
        self.projectpath = os.path.abspath('c:\\')
        self.object_prefix = self.txt_prefix.text()

    def updateUI(self):
        self.lbl_project.setText(self.projectpath)

    def select_project_folder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select project folder', self.projectpath)
        if directory:
            self.projectpath = os.path.abspath(directory)
            self.updateUI()

    def addCache(self):
        for node in MaxPlus.SelectionManager_GetNodes():
            cachename = os.path.join(self.projectpath, 'cache', str(self.object_prefix) + node.Name + '.pc2')
            if os.path.exists(cachename):
                mod = MaxPlus.Factory.CreateWorldSpaceModifier(MaxPlus.ClassIds.Point_CacheSpacewarpModifier)
                mod.ParameterBlock.Filename.Value = os.path.join(self.projectpath, 'cache', cachename)
                node.AddModifier(mod)


if __name__ == '__main__':
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()