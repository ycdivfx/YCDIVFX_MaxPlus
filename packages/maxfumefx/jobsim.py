import MaxPlus


class FumeFxJobSim:
    def __init__(self):
        """Class to represent a FumeFx Job in simulation mode"""
        pass

    def getfumefxgrids(self, prefix='fumefx'):
        nodes = []
        for node in MaxPlus.Core.GetRootNode().Children:
            if prefix in node.Name.lower():
                nodes.append(node)

        return nodes


    def sendjobffx(self, node):
        rs = MaxPlus.RenderSettings

        rs.CloseDialog()

        timetype= rs.GetTimeType()
        savefile = rs.GetSaveFile()
        height = rs.GetHeight()
        width = rs.GetWidth()

        rs.SetTimeType(1)
        rs.SetSaveFile(False)
        rs.SetHeight(25)
        rs.SetWidth(25)

        MaxPlus.Core.EvalMAXScript('$' + node.Name + '.BackBurnerSim = True')
        MaxPlus.Core.EvalMAXScript('SMTDSettings.JobName = GetFilenameFile(maxfilename) + \"_FFXSim_\" + ' + node.Name)
        MaxPlus.Core.EvalMAXScript('SMTDFunctions.SubmitJob()')
        MaxPlus.Core.EvalMAXScript('$' + node.Name + '.BackBurnerSim = False')

        rs.SetTimeType(timetype)
        rs.SetSaveFile(savefile)
        rs.SetHeight(height)
        rs.SetWidth(width)

    def simtodeadline(self):
        fumefx_containers = getfumefxgrids()
        for fumefx in fumefx_containers:
            sendjobffx(fumefx)