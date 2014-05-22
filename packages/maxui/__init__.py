import MaxPlus
from PySide import QtGui, QtCore


class _GCProtector(object):
    """
    Garbage protector for QWidget classes and subclasses.
    """
    widgets = []


def MaxWindow(widget):
    """
    Decorator for QWidget, making it work with 3dsmax.
    @param QWidget widget - Widget to be handled
    @return - The decorated class
    """
    orig_init = widget.__init__
    orig_show = widget.show

    def __init__(self, *args, **kwargs):
        defs = {'stylename': 'Plastique', 'theme': None, 'parented': False}
        orig_init(self, *args, **kwargs)
        defs.update(kwargs)
        # Make widget garbage collected.
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._parented = defs['parented']
        self._has_parent = False
        self._setupUI(defs['stylename'], defs['theme'])

    def _setupUI(self, stylename, theme):
        for control in self.children():
            if hasattr(control, 'setStyle'):
                control.setStyle(QtGui.QStyleFactory.create(stylename))

        # Dark theme detection.
        if theme is None and MaxPlus.Core.EvalMAXScript('((colorman.getcolor #window) * 255)[1] < 120'
                                                        ' and ((colorman.getcolor #window) * 255)[2] < 120'
                                                        ' and ((colorman.getcolor #window) * 255)[3] < 120'):
            theme = 'dark'
        else:
            theme = 'light'

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

    def show(self):
        if self not in _GCProtector.widgets:
            _GCProtector.widgets.append(self)
        orig_show(self)
        if self._parented and not self._has_parent:
            import ctypes
            capsule = self.effectiveWinId()
            ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
            ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(capsule)
            MaxPlus.Win32.Set3dsMaxAsParentWindow(ptr)
            self._has_parent = True

    widget._setupUI = _setupUI
    widget.show = show
    widget.__init__ = __init__
    return widget