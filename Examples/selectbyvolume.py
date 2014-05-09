import MaxPlus
from maxhelpers import BoundingBox

# Grab selected object to use as volume
obj = MaxPlus.SelectionManager.GetNode(0)

if obj:
    BoundingBox.SelectByVolume(obj)
else:
    print 'Select an object!'