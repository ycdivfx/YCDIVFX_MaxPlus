from nose.tools import assert_equal

import maxviewport


class test_vpgrab():
    @classmethod
    def setUpClass (self):
        self.vp = maxviewport.VpGrab()

    def testMethod_Gw(self):
        assert_equal(self.vp.method, 'gw')

    def testMethod_Viewport(self):
        self.vp.method = maxviewport.VpGrabType.viewport
        assert_equal(self.vp.method, 'viewport')

class test_vpgrabtype():
    @classmethod
    def setUpClass(self):
        self.vptype = maxviewport.VpGrabType

    def testGw(self):
        assert_equal(self.vptype.gw, 'gw')

    def testViewport(self):
        assert_equal(self.vptype.viewport, 'viewport')