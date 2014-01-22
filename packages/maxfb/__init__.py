from facepy import GraphAPI
import fbauth


class FbConnector():
    def __init__(self):
        self.token = fbauth.getAccessToken()
        self.graph = GraphAPI(self.token)

    def postImage(self, caption, filename):
        """Posts an image file into FB
        :param str caption: a valid string
        :param str filename: a valid path to an image file
        """
        try:
            fimage = open(filename, 'rb')
            self.graph.post(path="me/photos", caption=caption, source=fimage)
        except:
            print 'Error submitting image'

    def postMessage(self, text):
        """Posts a message into FB
        :param str text: a valid string
        """
        try:
            self.graph.post(path='me/feed', message=text)
        except:
            print 'There was an error posting the message'

    def getUsername(self):
        """Gets the current logged in username
        :rtype:  str
        """
        try:
            r = self.graph.get('me?fields=name')
            return r['name']
        except:
            print 'Error retrieving name'