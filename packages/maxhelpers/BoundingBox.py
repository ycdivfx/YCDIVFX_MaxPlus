"""
Based on the work of Eric Spevacek for Maya
http://technicallyitsart.wordpress.com/2013/12/28/maya-python-select-by-volume/
"""
import MaxPlus
import maxhelpers as mh


class BoundingBox():
    """ Helper class for bounding box-related calculations."""
    @classmethod
    def FromShape(cls, shapeObj):
        """ Constructor method to create a bounding box from a shape.
            :param MaxPlus.INode shapeObj: Node to extract bounding box
        """
        boundingBox = BoundingBox()
        bb = mh.GetWorldBoundBox(shapeObj)
        boundingBox.minX = bb.Min.X
        boundingBox.minY = bb.Min.Y
        boundingBox.minZ = bb.Min.Z
        boundingBox.maxX = bb.Max.X
        boundingBox.maxY = bb.Max.Y
        boundingBox.maxZ = bb.Max.Z
        return boundingBox
 
    def ContainsShape(self, shape):
        """ Returns whether or not a shape is intersecting with this bounding box.
        """
        shapeBB = BoundingBox.FromShape(shape)
        return (shapeBB.minX < self.maxX and shapeBB.maxX > self.minX) and \
               (shapeBB.minY < self.maxY and shapeBB.maxY > self.minY) and\
               (shapeBB.maxZ < self.maxZ and shapeBB.maxZ > self.minZ)


def SelectByVolume(volumeObj):
    """ Selects all transforms in the scene that are within the specified argument's bounding box volume. """

    # Create bounding box class from object
    boundingBox = BoundingBox.FromShape(volumeObj)

    # Get all scene objects asides from bounding box
    sceneObjs = [obj for obj in MaxPlus.Core.GetRootNode().Children
                 if obj != volumeObj]

    # Compare against every object in our scene to determine what is in our volume
    newSelection = MaxPlus.INodeTab()
    for obj in sceneObjs:
        # If the shape's bounding box intersects with the volume's bounding box
        if boundingBox.ContainsShape(obj):
            newSelection.Append(obj)

    # Update selection to nodes contained in volume
    if newSelection:
        MaxPlus.SelectionManager.ClearNodeSelection()
        MaxPlus.SelectionManager.SelectNodes(newSelection)