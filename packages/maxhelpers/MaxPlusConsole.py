"""
Reference: http://area.autodesk.com/blogs/chris/pyqt-ui-in-3ds-max-2014-extension
"""
from PySide import QtGui, QtCore
import MaxPlus

app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])


class _Widgets(object):
    """ Used to store all widget instances and protect them from the garbage collector """
    _instances = []


class _FocusFilter(QtCore.QObject):
    """ Used to filter events to properly manage focus in 3ds Max. This is a hack to deal with the fact
        that mixing Qt and Win32 causes focus events to not get triggered as expected. """

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            MaxPlus.CUI.DisableAccelerators()
        return False


class MaxWidget(QtGui.QMainWindow):
    """ Note: this does not work automatically when switching focus from the rest of 3ds Max
        to the PyQt UI. This is why we have to install an event filter. """

    #def focusInEvent(self, event):
    #    MaxPlus.CUI.DisableAccelerators()
    #
    #def focusOutEvent(self, event):
    #    MaxPlus.CUI.EnableAccelerators()

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        #_Widgets._instances.append(self)
        # Install an event filter. Keep the pointer in this object so it isn't collected, and can be removed. 
        self.filter = _FocusFilter(self)
        app.installEventFilter(self.filter)

    def closeEvent(self, event):
        if self in _Widgets._instances:
            _Widgets._instances.remove(self)
            # Very important, otherwise the application event filter will stick around for
        app.removeEventFilter(self.filter)


