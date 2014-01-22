def mxs_eval(args):
    """EvalMAXScript(wchar_t const * s, FPValue result) -> bool
    EvalMAXScript(wchar_t const * s) -> FPValue
    """
    import MaxPlus

    return MaxPlus.Core.EvalMAXScript(args)


class BitmapTypes(object):
    # Not allocated yet
    BMM_NO_TYPE = 0
    # 1-bit monochrome image
    BMM_LINE_ART = 1
    # 8-bit paletted image. Each pixel value is an index into the color table.
    BMM_PALETTED = 2
    # 8-bit grayscale bitmap.
    BMM_GRAY_8 = 3
    # 16-bit grayscale bitmap.
    BMM_GRAY_16 = 4
    # 16-bit true color image.
    BMM_TRUE_16 = 5
    # 32-bit color: 8 bits each for Red, Green, Blue, and Alpha.
    BMM_TRUE_32 = 6
    # 64-bit color: 16 bits each for Red, Green, Blue, and Alpha.
    BMM_TRUE_64 = 7
    # 24-bit color: 8 bits each for Red, Green, and Blue. Cannot be written to.
    BMM_TRUE_24 = 8
    # 48-bit color: 16 bits each for Red, Green, and Blue. Cannot be written to.
    BMM_TRUE_48 = 9
    # This is the YUV format - CCIR 601. Cannot be written to.
    BMM_YUV_422 = 10
    # Windows BMP 16-bit color bitmap. Cannot be written to.
    BMM_BMP_4 = 11
    # Padded 24-bit (in a 32 bit register). Cannot be written to.
    BMM_PAD_24 = 12
    # Padded 24-bit (in a 32 bit register). Cannot be written to.
    BMM_LOGLUV_32 = 13
    BMM_LOGLUV_24 = 14
    BMM_LOGLUV_24A = 15
    # The 'Real Pixel' format.
    BMM_REALPIX_32 = 16
    # 32-bit floating-point per component (non-compressed), RGB with or without alpha
    BMM_FLOAT_RGBA_32 = 17
    # 32-bit floating-point (non-compressed), monochrome/grayscale
    BMM_FLOAT_GRAY_32 = 18
    BMM_FLOAT_RGB_32 = 19
    BMM_FLOAT_A_32 = 20


class BitmapOpenMode(object):
    BMM_NOT_OPEN = 0 # Not opened yet
    BMM_OPEN_R = 1 # Read-only
    BMM_OPEN_W = 2 # Write-only. No reads will occur


class CopyImageOperations(object):
    # Copy image to current map size w/cropping if necessary.
    COPY_IMAGE_CROP = 0
    # This is a resize from 50x50 to 150x150 using this option.
    COPY_IMAGE_RESIZE_LO_QUALITY = 1
    # This is a resize from 50x50 to 150x150 using this option.
    COPY_IMAGE_RESIZE_HI_QUALITY = 2
    # Resize based on Image Input Options (BitmapInfo *)
    COPY_IMAGE_USE_CUSTOM = 3


class ImageFileType(object):
    """ Class that holds different image file types """
    JPG = '.jpg'
    TGA = '.tga'
    BMP = '.bmp'

def GetWorldBoundBox(node):
    """ Gets world boundingbox of node
        :param MaxPlus.INode node: a valid path to an image file, no extension required
        :rtype:  MaxPlus.Box3
    """
    import MaxPlus

    # Viewport Manager
    vm = MaxPlus.ViewportManager
    # Get active viewport
    av = vm.GetActiveViewport()

    return node.GetBaseObject().GetWorldBoundBox(node, av)

def GetLocalBoundBox(node):
    """ Gets local boundingbox of node
        :param MaxPlus.INode node: a valid path to an image file, no extension required
        :rtype:  MaxPlus.Box3
    """
    import MaxPlus

    # Viewport Manager
    vm = MaxPlus.ViewportManager
    # Get active viewport
    av = vm.GetActiveViewport()

    return node.GetBaseObject().GetLocalBoundBox(node, av)
