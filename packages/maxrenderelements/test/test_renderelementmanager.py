'''
Created on 11/11/2013

@author: dgsantana
'''
import unittest
import maxrenderelements


class Test(unittest.TestCase):

    def setUp(self):
        print 'Setup'
        self._rm = maxrenderelements.RenderElementManager()
        self._rm.RemoveAllElements()
        self._rm.Active = True
        self._rm.Display = True

    def tearDown(self):
        print 'Cleanup'
        self._rm.RemoveAllElements()
        self._rm = None

    def testElementCount(self):
        self._rm.RemoveAllElements()
        self.failUnless(len(self._rm) == 0)

    def testAddElement(self):
        self._rm.RemoveAllElements()
        self._rm.AddElement('alphaRenderElement')
        self.failIf(len(self._rm) == 0)

    def testElementMXSProperty(self):
        self._rm.RemoveAllElements()
        element = self._rm.AddElement('ZRenderElement')
        self.failUnless(element.zMin == 100)

    def testActive(self):
        self._rm.Active = False
        self.failUnless(self._rm.Active == False)

    def testDisplay(self):
        self._rm.Display = False
        self.failUnless(self._rm.Display == False)


if __name__ == "__main__":
    unittest.main()
