import MaxPlus


def getselectednodenames():
    for node in MaxPlus.SelectionManager.Nodes:
        print node.Name

def getscenenodenames():
    for node in MaxPlus.Core.GetRootNode().Children:
        print node.Name

if __name__ == '__main__':
    getselectednodenames()
    getscenenodenames()