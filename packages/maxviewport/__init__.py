try:
    import MaxPlus
except ImportError:
    print 'MaxPlus not present'


class VpGrabType():
    """Enumerates the method used for viewport grabbing.
    viewport method allows you to grab the viewport with Depht of field and Motion Blur because it includes the results
    of maxops.displayActiveCameraViewWithMultiPassEffect()
    """
    gw = "gw"
    viewport = "viewport"



class VpGrab():
    def __init__(self, method=VpGrabType.gw):
        """This class provides you methods to grab the 3dsmax viewport"""
        self.method = method
        pass

    def tofile(self, filename):
        """Grabs viewport to a file on the hard-drive."""
        MaxPlus.Core_EvalMAXScript('''grab = ''' + self.method + '''.GetViewportDIB()
        grab.filename = @"''' + filename + '''"
        save grab
        close grab''')
        return True

    def toclipboard(self):
        """Grabs viewport to the clipboard."""
        MaxPlus.Core_EvalMAXScript('''grab = ''' + self.method + '''.GetViewportDIB()
        setclipboardbitmap grab
        close grab''')
        return True