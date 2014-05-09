import maxfb


if __name__ == '__main__':
    fbc = maxfb.FbConnector()

    print 'Your Facebook username is:' + fbc.getUsername()

    #message = '3dsmax python connector with automatic authentication'
    #fbc.postMessage(message)
    #imagefilename = r'c:\test.jpg'
    #fbc.postImage('', imagefilename)