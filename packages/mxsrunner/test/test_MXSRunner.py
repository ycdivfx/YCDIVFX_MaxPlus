import os
from nose.tools import assert_equal

import mxsrunner


class test_mxssettings():
    @classmethod
    def setUpClass (self):
        self.CURRPATH = os.path.dirname(os.path.abspath(__file__))
        self.mxs = mxsrunner.MxsSettings()

    def testLoad(self):
        res = self.mxs.load(os.path.join(self.CURRPATH, 'testdata', 'settings.ini'))
        assert_equal(res, None)

    def testLoadMissingFile(self):
        res = self.mxs.load(os.path.join(self.CURRPATH, 'testdata', 'settings1.ini'))
        assert_equal(len(self.mxs.config._sections), 0)

    def testGetConfig(self):
        self.mxs.load(os.path.join(self.CURRPATH, 'testdata', 'settings.ini'))
        filename = self.mxs.getconfig('Settings', 'Filename')

        assert_equal(filename, 'main.py')

    def testSetConfig(self):
        self.mxs.load(os.path.join(self.CURRPATH, 'testdata', 'settings.ini'))
        res = self.mxs.setconfig('Settings', 'Filename', 'main.py')

        assert_equal(res, True)
