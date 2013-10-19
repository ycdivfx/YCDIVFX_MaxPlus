import os

from mxssettings import *


class MxsRunner:
    def __init__(self, path):
        self.CURRPATH = os.path.abspath(path)
        self.settings = MxsSettings()
        self.settings.load(os.path.join(self.CURRPATH, 'settings.ini'))

        self.RUNMS = os.path.join(self.CURRPATH, 'run.ms')
        self.EXTERNAL = os.path.join(self.settings.getconfig('Settings', 'External'), 'ExternalMaxScriptIDE.exe')

    def run(self):
        import subprocess

        callparams = [self.EXTERNAL, self.RUNMS]
        subprocess.call(callparams)