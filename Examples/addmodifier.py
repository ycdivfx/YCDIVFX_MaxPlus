import MaxPlus


def addmodifier(nodes):
    for node in nodes:
        mod = MaxPlus.Factory.CreateObjectModifier(MaxPlus.ClassIds.Noisemodifier)
        for param in  mod.ParameterBlock:
            print param.Name
        mod.ParameterBlock.seed.Value = 12345
        node.AddModifier(mod)

if __name__ == '__main__':
    addmodifier(MaxPlus.SelectionManager.Nodes)