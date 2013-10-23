try:
    import MaxPlus
except ImportError:
    MaxPlus = None
    print 'MaxPlus not present'

import maxfumefx
reload(maxfumefx)


class FumeFxJobSim:
    def __init__(self):
        """Class to represent a FumeFx Job in simulation mode"""
        pass

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
        MaxPlus.Core.EvalMAXScript('SMTDSettings.JobName = GetFilenameFile(maxfilename) + \"_FFXSim_' + node.Name + '\"')
        MaxPlus.Core.EvalMAXScript('SMTDFunctions.SubmitJob()')
        MaxPlus.Core.EvalMAXScript('$' + node.Name + '.BackBurnerSim = False')

        rs.SetTimeType(timetype)
        rs.SetSaveFile(savefile)
        rs.SetHeight(height)
        rs.SetWidth(width)

    def simtodeadline(self):
        fumefx_containers = maxfumefx.getfumefxgrids()
        for fumefx in fumefx_containers:
            self.sendjobffx(fumefx)