import maxfumefx
import maxfumefx.jobsim as js
reload(maxfumefx)
reload(maxfumefx.jobsim)

ffxsim = js.FumeFxJobSim()

ffxsim.simtodeadline()
