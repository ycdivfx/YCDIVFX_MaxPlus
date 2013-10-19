import maxfb

if __name__ == '__main__':
    fbc = maxfb.FbConnector()

    print 'Your Facebook username is:' + fbc.getusername()

    message = '3dsmax python connector with automatic authentication'
    fbc.postmessage(message)
    imagefilename = r'c:\test.jpg'
    fbc.postimage('', imagefilename)