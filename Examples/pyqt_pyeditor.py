import os
from PyQt4 import QtGui, uic, QtCore
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

import MaxPlus


def getscriptpath():
    pkgdir = os.path.dirname(os.path.abspath(__file__))
    return pkgdir

PACKAGEDIR = getscriptpath()

MainWindowForm, MainWindowBase = uic.loadUiType(
    os.path.join(getscriptpath(), 'ui', 'editor.ui'))


def formatstringtomaxscript(code):
    code = code.replace('\"', '\'')
    code = code.replace('\\', '\\\\')
    res = 'python.Execute("%s")' % code
    return res


class MainWindow(MainWindowBase, MainWindowForm):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.font = QtGui.QFont()
        self.setupui(self.textEdit, self.font)
        self.lexer = QsciLexerPython()

        self.textEdit.setLexer(self.lexer)
        self.textEdit.setText(r'''import MaxPlus
# Look in the MAXScript listener
MaxPlus.Core.WriteLine("hello world")''')

        self.btn_run.triggered.connect(self.editorrun)
        self.btn_clear.triggered.connect(self.editorclear)
        self.actionOpen.triggered.connect(self.loadfile)

        self.connect(self.tabWidget, QtCore.SIGNAL('tabCloseRequested(int)'), self.closetab)


    def setupui(self, editor, font):
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

    def newtab(self, tw, tname):
        newtab = QtGui.QWidget()
        vlayout = QtGui.QVBoxLayout()
        vlayout.setMargin(0)

        neweditor = QsciScintilla(newtab)
        neweditor.setStyleSheet("border:0")
        self.setupui(neweditor, self.font)
        neweditor.setLexer(self.lexer)

        vlayout.addWidget(neweditor)
        newtab.setLayout(vlayout)

        return tw.addTab(newtab, os.path.basename(str(tname))), neweditor

    def loadfile(self):
        fname = QtGui.QFileDialog.getOpenFileName(
            self, 'Open file', os.path.join(PACKAGEDIR, '..\Examples'))

        f = open(fname, 'r')
        with f:
            idx, neweditor = self.newtab(self.tabWidget, os.path.basename(str(fname)))
            self.tabWidget.setCurrentIndex(idx)
            data = f.read()
            neweditor.setText(data)

    def closetab(self, idx):
        if self.tabWidget.count() != 1:
            self.tabWidget.removeTab(idx)

    def gettabtext(self):
        ctab = self.tabWidget.currentWidget()
        for idx, child in enumerate(ctab.children()):
            if type(child) is type(QsciScintilla()):
                return child.text()

    def editorrun(self):
        pycode = str(self.gettabtext())
        MaxPlus.Core.EvalMAXScript(formatstringtomaxscript(pycode))

    def editorclear(self):
        MaxPlus.Core.EvalMAXScript('clearListener()')


class _FocusFilter(QtCore.QObject):
    """ Used to filter events to properly manage focus in 3ds Max. This is a hack to deal with the fact
        that mixing Qt and Win32 causes focus events to not get triggered as expected. """

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            MaxPlus.CUI.DisableAccelerators()
        return False


if __name__ == '__main__':
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    # Install filter so we can disable 3dsMax accelerators everytime we focus on our Script Editor
    filter = _FocusFilter()
    app.installEventFilter(filter)

    window = MainWindow()
    window.show()
