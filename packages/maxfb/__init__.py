from facepy import GraphAPI
import fbauth


class FbConnector():
    def __init__(self):
        self.token = fbauth.getaccesstoken()
        self.graph = GraphAPI(self.token)

    def postimage(self, caption, filename):
        try:
            fimage = open(filename, 'rb')
            self.graph.post(path="me/photos", caption=caption, source=fimage)
        except:
            print 'Error submitting image'

    def postmessage(self, text):
        try:
            self.graph.post(path='me/feed', message=text)
        except:
            print 'There was an error posting the message'

    def getusername(self):
        try:
            r = self.graph.get('me?fields=name')
            return r['name']
        except:
            print 'Error retrieving name'