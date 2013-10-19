import os
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

import MaxPlus

MAX_DEBUG = False


def debugMode():
    pydev_path = r'C:\Program Files (x86)\JetBrains\PyCharm 3.0\helpers'
    if not pydev_path in sys.path:
        sys.path.append(pydev_path)

    from pydev import pydevd
    pydevd.settrace('localhost', port=7720, suspend=False)

if MAX_DEBUG:
    debugMode()


def getScriptPath():
    pkgdir = os.path.dirname(os.path.abspath(__file__))
    return pkgdir

PACKAGEDIR = getScriptPath()


def get3dsmaxHWND():
    """
    Gets the main 3dsmax window handle
    """
    return MaxPlus.Core_GetWindowHandle()


MainWindowForm, MainWindowBase = uic.loadUiType(
    os.path.join(getScriptPath(), 'ui', 'editor.ui'))


def mxsExecutePython(code):
    code = code.replace('\r\n', '\n')
    code = code.replace(r'"', '\'')
    formattedcode = ''
    #for line in code.split('\n'):
    #    formattedcode += line + '\n'
    print formattedcode
    fne = 'python.Execute("' + code + '")'
    return fne


class MainWindow(MainWindowBase, MainWindowForm):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.font = QtGui.QFont()
        self.setupUiEditor(self.textEdit, self.font)
        self.lexer = QsciLexerPython()

        self.textEdit.setLexer(self.lexer)
        self.textEdit.setText(r'''import MaxPlus
# Look in the MAXScript listener
MaxPlus.Core.WriteLine("hello world")''')

        self.btn_run.triggered.connect(self.editorRun)
        self.btn_clear.triggered.connect(self.editorClear)
        self.actionOpen.triggered.connect(self.loadFile)

        self.connect(self.tabWidget, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeTab)

    def setupUiEditor(self, editor, font):
        ## define the font to use

        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(10)
        # the font metrics here will help
        # building the margin width later
        fm = QtGui.QFontMetrics(font)

        ## set the default font of the editor
        ## and take the same font for line numbers
        editor.setFont(font)
        editor.setMarginsFont(font)

        ## Line numbers
        # conventionnaly, margin 0 is for line numbers
        editor.setMarginWidth(0, fm.width('0000'))

        ## Edge Mode shows a red vetical bar at 80 chars
        editor.setEdgeMode(QsciScintilla.EdgeLine)
        editor.setEdgeColumn(80)
        editor.setEdgeColor(QtGui.QColor('LightGray'))

        ## Folding visual : we will use boxes
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ## Editing line color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QtGui.QColor('LightYellow'))

        ## Margins colors
        # line numbers margin
        editor.setMarginsBackgroundColor(QtGui.QColor('LightGray'))
        editor.setMarginsForegroundColor(QtGui.QColor('DarkRed'))

        # folding margin colors (foreground,background)
        editor.setFoldMarginColors(QtGui.QColor('Lime'),QtGui.QColor('White'))

    def addNewTab(self, tw, tname):
        newtab = QtGui.QWidget()
        vlayout = QtGui.QVBoxLayout()
        vlayout.setMargin(0)

        neweditor = QsciScintilla(newtab)
        neweditor.setStyleSheet("border:0")
        self.setupUiEditor(neweditor, self.font)
        neweditor.setLexer(self.lexer)

        vlayout.addWidget(neweditor)
        newtab.setLayout(vlayout)

        return tw.addTab(newtab, os.path.basename(str(tname))), neweditor

    def loadFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(
            self, 'Open file', os.path.join(PACKAGEDIR, '..\Examples'))

        f = open(fname, 'r')
        with f:
            idx, neweditor = self.addNewTab(self.tabWidget, os.path.basename(str(fname)))
            self.tabWidget.setCurrentIndex(idx)
            data = f.read()
            neweditor.setText(data)
            neweditor.tri

    def closeTab(self, idx):
        if self.tabWidget.count() != 1:
            self.tabWidget.removeTab(idx)

    def getCurrentTabScript(self):
        ctab = self.tabWidget.currentWidget()
        for idx, child in enumerate(ctab.children()):
            if type(child) is type(QsciScintilla()):
                return child.text()

    def editorRun(self):
        pycode = str(self.getCurrentTabScript())
        MaxPlus.Core.EvalMAXScript(mxsExecutePython(pycode))

    def editorClear(self):
        MaxPlus.Core.EvalMAXScript('clearListener()')


if __name__ == '__main__':
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    window = MainWindow()
    window.show()
