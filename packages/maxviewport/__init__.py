import MaxPlus
from maxhelpers import mxs_eval, BitmapTypes, ImageFileType


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

    def ActiveViewport(self, name=(MaxPlus.PathManager.GetRenderOutputDir()
                                   + r'\default'), FileType=ImageFileType.JPG):
        """Grabs viewport to a file on the hard-drive.

        :param str name: a valid path to an image file, no extension required
        :param ImageFileType FileType: one of the available types in ImageFileType

        :rtype:  MaxPlus.Bitmap
        """
        # Create storage
        storage = MaxPlus.Factory.CreateStorage(BitmapTypes.BMM_LINE_ART)

        # Create BitmapInfo
        bmi = storage.GetBitmapInfo()
        # Set filename
        bmi.SetName(name + FileType)

        print bmi.GetName()

        # Create bitmap to hold the dib
        bmp = MaxPlus.Factory.CreateBitmap()

        # Viewport Manager
        vm = MaxPlus.ViewportManager
        # Get active viewport
        av = vm.GetActiveViewport()
        # Grab the viewport dib into the bitmap
        av.GetDIB(bmi, bmp)

        # Open bitmap for writing
        bmp.OpenOutput(bmi)
        # Save to file
        bmp.Write(bmi)
        # Close bitmap
        bmp.Close(bmi)

        return bmp

    def tofile(self, filename):
        """Grabs viewport to a file on the hard-drive."""
        args = '''grab = ''' + self.method + '''.GetViewportDIB()
        grab.filename = @"''' + filename + '''"
        save grab
        close grab'''
        mxs_eval(args)

    def toclipboard(self):
        """Grabs viewport to the clipboard."""
        args = '''grab = ''' + self.method + '''.GetViewportDIB()
        setclipboardbitmap grab
        close grab'''
        mxs_eval(args)