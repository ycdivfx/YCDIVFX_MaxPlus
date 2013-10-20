import maxviewport as mv
#Prevent having to restart 3dsmax after changes in the .py files
reload(mv)

if __name__ == '__main__':
    #Example using gw method of viewport grabbing (default for this class)
    vpGrab = mv.VpGrab()
    vpGrab.tofile(r'c:\test_gw.jpg')
    vpGrab.toclipboard()

    #Example using viewport method of viewport grabbing (default for this class)
    vpGrab = mv.VpGrab(mv.VpGrabType.viewport)
    vpGrab.tofile(r'c:\test_viewport.jpg')
    vpGrab.toclipboard()