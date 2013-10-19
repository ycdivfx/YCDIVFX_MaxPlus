from ConfigParser import *


class MyCasePreservingConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

class MxsSettings:
    def __init__(self):
        self.config = None
        self.filename = None

    def load(self, filename):

        config = MyCasePreservingConfigParser()
        config.read(filename)
        self.filename = filename
        self.config = config

    def getconfig(self, section, option):
        if self.config:
            return self.config.get(section, option)

    def setconfig(self, section, option, value):
        if self.config:
            self.config.set(section, option, value)
            with open(self.filename, 'w') as configfile:
                self.config.write(configfile)
                return True