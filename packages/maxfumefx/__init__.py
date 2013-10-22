import MaxPlus


def getfumefxgrids(prefix='fumefx'):
    """Helper function that returns a list with all FumeFx Grids in the scene
    Note: I still need to figure out if we can match the object class against the fumefx class, which would be better.
    """
    nodes = []
    for node in MaxPlus.Core.GetRootNode().Children:
        if 'fumefx' in prefix:
            nodes.append(node)

    return nodes