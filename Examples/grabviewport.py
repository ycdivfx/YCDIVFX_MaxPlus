import maxviewport


if __name__ == '__main__':
    vpGrab = maxviewport.VpGrab()
    bmp = vpGrab.ActiveViewport()
    bmp.Display()
