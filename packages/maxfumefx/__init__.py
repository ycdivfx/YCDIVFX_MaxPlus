try:
    import MaxPlus
except ImportError:
    MaxPlus = None
    print 'MaxPlus not present'


def getfumefxgrids():
    """Helper function that returns a list with all FumeFx Grids in the scene
    """
    nodes = []
    for node in MaxPlus.Core.GetRootNode().Children:
        if 'fumefx' in node.Object.GetClassName().lower():
            nodes.append(node)

    return nodes