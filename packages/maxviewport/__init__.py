import MaxPlus
from maxhelpers import mxs_eval, BitmapTypes, ImageFileType, CopyImageOperations

'''
To disable button labels in maxscript: ViewportButtonMgr.EnableButtons = False
'''

class VpGrabType():
    """
    Enumerates the method used for viewport grabbing.
    viewport method allows you to grab the viewport with Depht of field and Motion Blur because it includes the results
    of maxops.displayActiveCameraViewWithMultiPassEffect()
    """
    gw = "gw"
    viewport = "viewport"


class VpGrab():
    def __init__(self, method=VpGrabType.gw):
        """This class provides you methods to grab the 3dsmax viewport"""
        self.method = method

    def ActiveViewport(self, filename=(MaxPlus.PathManager.GetRenderOutputDir()
                                   + r'\default.jpg')):
        """Grabs viewport to a file on the hard-drive using default viewport size.

        :param str filename: a valid path to an image file

        :rtype:  MaxPlus.Bitmap
        """
        # Create storage
        storage = MaxPlus.Factory.CreateStorage(BitmapTypes.BMM_TRUE_64)

        # Create BitmapInfo
        bmi = storage.GetBitmapInfo()

        # Set filename
        bmi.SetName(filename)

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
        bmp.Write(bmi)
        bmp.Close(bmi)

        return bmp

    def ActiveViewportSize(self, filename=(MaxPlus.PathManager.GetRenderOutputDir()
                                   + r'\default.jpg'), size=(640, 480)):
        """Grabs viewport to a file on the hard-drive in a specific size.

        :param str filename: a valid path to an image file
        :param tuple size: a valid list containing width and height
        :rtype:  MaxPlus.Bitmap
        """
        # Create storage
        storage = MaxPlus.Factory.CreateStorage(BitmapTypes.BMM_TRUE_64)

        # Create BitmapInfo
        bmi = storage.GetBitmapInfo()

        # Create bitmap to hold the dib
        grab = MaxPlus.Factory.CreateBitmap()

        # Viewport Manager
        vm = MaxPlus.ViewportManager
        # Get active viewport
        av = vm.GetActiveViewport()
        # Grab the viewport dib into the bitmap
        av.GetDIB(bmi, grab)

        # Set filename & Size
        bmi.SetName(filename)
        bmi.SetWidth(size[0])
        bmi.SetHeight(size[1])

        # Create new bitmap to hold the resized version
        bmp = MaxPlus.Factory.CreateBitmap(bmi)
        bmp.CopyImage(grab, CopyImageOperations.COPY_IMAGE_RESIZE_HI_QUALITY, 1)
        grab.Close(bmi)

        # Open bitmap for writing
        bmp.OpenOutput(bmi)
        bmp.Write(bmi)
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